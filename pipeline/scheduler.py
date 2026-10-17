# -- coding: utf-8 --
# pipeline/scheduler.py - Scheduler nhe (thread + DB + worker dispatch)
# P0 hardening: unified run(interval, stop_event), atomic dispatch, cron fix,
# Asia/Saigon tz normalization, pause/resume, surfaced errors.
import os, sys, time, threading, json, subprocess, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state
try:
	from pipeline import auto_publish as _ap
except Exception:
	_ap = None

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


def drain_pending():
	c = state.connect()
	try:
		rows = c.execute('SELECT id, status, run_at FROM jobs WHERE status IN (?,?) ORDER BY priority ASC, created_at ASC', ('pending','scheduled')).fetchall()
	except Exception:
		rows = []
	c.close()
	now_dt = _now_local()
	due_rows = []
	for r in rows:
		if r['status'] == 'pending':
			due_rows.append(r)
		else:
			dt = _parse_run_at(r['run_at'])
			if dt is not None and dt <= now_dt:
				due_rows.append(r)
	started = []
	for r in due_rows:
		if dispatch_job(r['id']):
			started.append(r['id'])
	return len(started)

STATUS_PATH = os.path.join(ROOT, 'state', 'scheduler_status.json')


def _write_status(alive=True, last_tick_created=0):
	payload = {'alive': bool(alive), 'last_tick': state.now(), 'last_created': int(last_tick_created), 'last_error': dict(LAST_ERROR), 'pid': os.getpid()}
	try:
		os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
		json.dump(payload, open(STATUS_PATH, 'w', encoding='utf-8'), ensure_ascii=False)
	except Exception:
		pass

def _first_kind(row):
	try:
		ks = row['kinds']
		if isinstance(ks, str):
			ks = json.loads(ks or '[]')
		if isinstance(ks, list) and ks:
			return str(ks[0])
	except Exception:
		pass
	return 'short'


def tick():
	# Daily auto-cleanup (publish-qua-14-ngay hoac >2GB)
	try:
		import os, time
		from ops import auto_cleanup as _ac
		stamp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'state', 'last_cleanup.txt')
		last = 0
		if os.path.exists(stamp):
			last = os.path.getmtime(stamp)
		if time.time() - last > 86400:
			r = _ac.run(dry_run=False)
			open(stamp, 'w').write(str(int(time.time())))
			if r.get('moved'):
				print('[scheduler] cleanup moved ' + str(r['moved']) + ' files')
	except Exception as _e:
		pass
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
	# run_at jobs duoc xu ly boi drain_pending() (chi dispatch job due), tranh trung
	pass
	rows = c.execute('SELECT id, schedule, kinds FROM channels WHERE enabled=1').fetchall()
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
				(jid, r['id'], sched.get('kind') or _first_kind(r), sched.get('topic', ''),
				 'pending', state.now(), int(sched.get('count', 1)), int(sched.get('require_approval', 1))),
			)
			c.commit()
			if dispatch_job(jid):
				created.append(jid)
		except Exception as e:
			_note_error('create job fail ' + str(r['id']) + ': ' + str(e))
	c.close()
	# Advisor refresh (moi 30 phut)
	try:
		import time as _t, os as _os
		_c = _os.path.join(ROOT, 'state', 'studio_advisor_cache.json')
		_age = (_t.time() - _os.path.getmtime(_c)) if _os.path.exists(_c) else 1e9
		if _age > 1800:
			from ops import studio_advisor as _sa
			_sa.analyze(force=True)
	except Exception:
		pass

	# Recovery stale jobs (running > 5 min)
	try:
		from pipeline import recovery as _rec
		_rec.recover_stale_jobs(300)
	except Exception:
		pass
	# Auto-verify published videos (moi 15 phut) — phat hien video bi YouTube go
	try:
		import os as _os2, time as _t2
		_vstamp = _os2.path.join(ROOT, 'state', 'last_verify.txt')
		_vlast = _os2.path.getmtime(_vstamp) if _os2.path.exists(_vstamp) else 0
		if _t2.time() - _vlast > 900:
			from pipeline import verify_pubs as _vp
			_vr = _vp.verify_pending(limit=100)
			open(_vstamp, 'w').write(str(_t2.time()))
			if _vr.get('dead', 0) > 0:
				_note_error('verify: ' + str(_vr.get('dead')) + ' video khong con tren YouTube')
	except Exception:
		pass
	drained = drain_pending()
	published = 0
	if _ap:
		try:
			published = _ap.publish_due()
		except Exception:
			published = 0
	_write_status(True, len(created) + drained + published)
	return len(created) + drained + published


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
