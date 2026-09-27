# -- coding: utf-8 --
# pipeline/scheduler.py - Scheduler nhe (thread + DB + worker dispatch)
# P0 hardening: unified run(interval, stop_event), atomic dispatch, cron fix,
# Asia/Saigon tz normalization, pause/resume, surfaced errors.
import os, sys, time, threading, json, subprocess, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state

try:
	from zoneinfo import ZoneInfo
	TZ = ZoneInfo('Asia/Saigon')
except Exception:
	TZ = None

STARMARK = chr(42)
SLASHMARK = chr(47)

LAST_ERROR = {'msg': '', 'ts': ''}
RUNNING = {}
RUNNING_LOCK = threading.Lock()
MAX_CONCURRENT = 2


def _note_error(msg):
	LAST_ERROR['msg'] = str(msg)[:300]
	LAST_ERROR['ts'] = state.now()
	try:
		print('[scheduler] ERR: ' + LAST_ERROR['msg'])
	except Exception:
		pass


def last_error():
	return dict(LAST_ERROR)


def _now_local():
	if TZ is not None:
		return datetime.datetime.now(TZ)
	return datetime.datetime.now()


def _expand_cron_field(field, lo, hi):
	if field == STARMARK:
		return set(range(lo, hi + 1))
	out = set()
	for part in field.split(','):
		part = part.strip()
		if not part:
			continue
		step = 1
		if SLASHMARK in part:
			base, sp = part.split(SLASHMARK, 1)
			try:
				step = int(sp)
			except Exception:
				return None
			if step <= 0:
				return None
			part = base
		if part == STARMARK:
			start, end = lo, hi
		elif '-' in part:
			a, b = part.split('-', 1)
			try:
				start, end = int(a), int(b)
			except Exception:
				return None
		else:
			try:
				start = end = int(part)
			except Exception:
				return None
		if start < lo or end > hi or start > end:
			return None
		v = start
		while v <= end:
			out.add(v)
			v += step
	return out


def parse_cron(expr):
	p = (expr or '').split()
	if len(p) != 5:
		return None
	try:
		res = {
			'minute': _expand_cron_field(p[0], 0, 59),
			'hour': _expand_cron_field(p[1], 0, 23),
			'day': _expand_cron_field(p[2], 1, 31),
			'month': _expand_cron_field(p[3], 1, 12),
			'weekday': _expand_cron_field(p[4], 0, 6),
		}
	except Exception:
		return None
	for v in res.values():
		if v is None:
			return None
	return res


def due_now(cron, now=None):
	parsed = parse_cron(cron)
	if not parsed:
		return False
	if now is None:
		now = _now_local()
	minute = now.tm_min if hasattr(now, 'tm_min') else now.minute
	hour = now.tm_hour if hasattr(now, 'tm_hour') else now.hour
	mday = now.tm_mday if hasattr(now, 'tm_mday') else now.day
	mon = now.tm_mon if hasattr(now, 'tm_mon') else now.month
	wd = now.tm_wday if hasattr(now, 'tm_wday') else now.weekday()
	if minute not in parsed['minute']:
		return False
	if hour not in parsed['hour']:
		return False
	if mday not in parsed['day']:
		return False
	if mon not in parsed['month']:
		return False
	cron_to_py = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
	allowed = {cron_to_py[c] for c in parsed['weekday']}
	if wd not in allowed:
		return False
	return True


def _parse_run_at(s):
	if not s:
		return None
	for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M'):
		try:
			dt = datetime.datetime.strptime(s, fmt)
			if TZ is not None and dt.tzinfo is None:
				dt = dt.replace(tzinfo=TZ)
			return dt
		except Exception:
			continue
	return None


def _claim_job(job_id, from_statuses=('scheduled', 'pending')):
	c = state.connect()
	try:
		ph = ','.join('?' for _ in from_statuses)
		cur = c.execute(
			'UPDATE jobs SET status=?, updated_at=? WHERE id=? AND status IN (' + ph + ')',
			('running', state.now(), job_id) + tuple(from_statuses),
		)
		c.commit()
		return cur.rowcount == 1
	finally:
		c.close()


def _active_count():
	with RUNNING_LOCK:
		dead = [k for k, p in RUNNING.items() if p.poll() is not None]
		for k in dead:
			RUNNING.pop(k, None)
		return len(RUNNING)


def dispatch_job(job_id, requeue_on_full=False):
	if _active_count() >= MAX_CONCURRENT:
		return False
	c = state.connect()
	row = c.execute(
		'SELECT id, channel_id, kind, topic, length_override, voice_override, music_mood, count, require_approval, status FROM jobs WHERE id=?',
		(job_id,),
	).fetchone()
	if not row:
		c.close()
		return False
	if row['status'] not in ('scheduled', 'pending'):
		c.close()
		return False
	job_dict = {
		'job_id': row['id'], 'channel_id': row['channel_id'], 'kind': row['kind'],
		'topic': row['topic'], 'length_override': row['length_override'],
		'voice_override': row['voice_override'], 'music_mood': row['music_mood'],
		'count': row['count'], 'require_approval': bool(row['require_approval']),
		'created_by': 'scheduler',
	}
	c.close()
	if not _claim_job(job_id):
		return False
	cmd = [sys.executable, '-m', 'pipeline.runner', '--job-json', json.dumps(job_dict, ensure_ascii=False)]
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	logdir = os.path.join(ROOT, 'logs')
	os.makedirs(logdir, exist_ok=True)
	log = os.path.join(logdir, 'scheduler.log')
	try:
		f = open(log, 'a', encoding='utf-8')
		f.write('[scheduler] spawn ' + job_id + ' at ' + state.now() + chr(10))
		f.flush()
		p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	except Exception as e:
		_note_error('spawn fail ' + job_id + ': ' + str(e))
		cc = state.connect()
		cc.execute('UPDATE jobs SET status=?, error=? WHERE id=?', ('failed', str(e)[:200], job_id))
		cc.commit()
		cc.close()
		return False
	with RUNNING_LOCK:
		RUNNING[job_id] = p
	cc = state.connect()
	cc.execute('UPDATE jobs SET status=?, error=?, updated_at=? WHERE id=? AND status=?',
		('running', 'spawned pid=' + str(p.pid), state.now(), job_id, 'running'))
	cc.commit()
	cc.close()
	return True


def _paused():
	return os.path.exists(os.path.join(ROOT, 'state', 'paused.flag'))


def tick():
	if _paused():
		return 0
	now = _now_local()
	c = state.connect()
	created = []
	try:
		rows_at = c.execute(
			'SELECT id, run_at FROM jobs WHERE status=? AND run_at IS NOT NULL',
			('scheduled',),
		).fetchall()
	except Exception:
		rows_at = []
	for r in rows_at:
		due = parse_run_at(r['run_at'])
		if due is None:
			continue
		if due <= now:
			if dispatch_job(r['id']):
				created.append(r['id'])
	rows = c.execute('SELECT id, schedule FROM channels WHERE enabled=1').fetchall()
	for r in rows:
		try:
			sched = json.loads(r['schedule'] or '{}')
		except Exception:
			sched = {}
		cron = sched.get('cron') or sched.get('scheduleCron') or ''
		if not due_now(cron, now):
			continue
		try:
			jid = 'job' + now.strftime('%Y%m%d%H%M') + '' + str(r['id'])[:8]
			existing = c.execute('SELECT 1 FROM jobs WHERE id=?', (jid,)).fetchone()
			if existing:
				continue
			c.execute(
				'INSERT INTO jobs (id, channel_id, kind, topic, status, created_at, count, require_approval) VALUES (?,?,?,?,?,?,?,?)',
				(jid, r['id'], sched.get('kind', 'short'), sched.get('topic', ''),
				 'pending', state.now(), int(sched.get('count', 1)), int(sched.get('require_approval', 1))),
			)
			c.commit()
			if dispatch_job(jid):
				created.append(jid)
		except Exception as e:
			_note_error('create job fail ' + str(r['id']) + ': ' + str(e))
	c.close()
	return len(created)


def run(interval=30, stop_event=None):
	while True:
		if stop_event is not None and stop_event.is_set():
			break
		try:
			n = tick()
			if n:
				print('[scheduler] tick created=' + str(n))
		except Exception as e:
			_note_error('tick: ' + str(e))
		if stop_event is not None:
			if stop_event.wait(interval):
				break
		else:
			time.sleep(interval)


def loop_forever(interval=30):
	run(interval=interval, stop_event=None)


if __name__ == '__main__':
	run(interval=30)
