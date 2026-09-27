# -- coding: utf-8 --
# pipeline/scheduler.py - Scheduler nhe (thread + DB + worker dispatch)
import os, sys, time, threading, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state

STARMARK = chr(42)
SLASHMARK = chr(47)


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
				step = 1
			part = base
		if part == STARMARK:
			rng = range(lo, hi + 1)
		elif '-' in part:
			a, b = part.split('-', 1)
			rng = range(int(a), int(b) + 1)
		else:
			rng = [int(part)]
		out.update(v for v in rng if lo <= v <= hi and ((v - lo) % step == 0 or step == 1))
	return out


def parse_cron(expr):
	p = (expr or '').split()
	if len(p) != 5:
		return None
	try:
		return {
			'minute': _expand_cron_field(p[0], 0, 59),
			'hour': _expand_cron_field(p[1], 0, 23),
			'day': _expand_cron_field(p[2], 1, 31),
			'month': _expand_cron_field(p[3], 1, 12),
			'weekday': _expand_cron_field(p[4], 0, 6),
		}
	except Exception:
		return None


def due_now(cron, now):
	parsed = parse_cron(cron)
	if not parsed:
		return False
	if now.tm_min not in parsed['minute']:
		return False
	if now.tm_hour not in parsed['hour']:
		return False
	if now.tm_mday not in parsed['day']:
		return False
	if now.tm_mon not in parsed['month']:
		return False
	cron_to_tm = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
	allowed_tm = {cron_to_tm[c] for c in parsed['weekday']}
	if now.tm_wday not in allowed_tm:
		return False
	return True


def dispatch_job(job_id):
	c = state.connect()
	row = c.execute('SELECT id, channel_id, kind, topic, length_override, voice_override, music_mood, count, require_approval FROM jobs WHERE id=?', (job_id,)).fetchone()
	if not row:
		return False
	job_dict = {
		'job_id': row['id'], 'channel_id': row['channel_id'], 'kind': row['kind'],
		'topic': row['topic'], 'length_override': row['length_override'],
		'voice_override': row['voice_override'], 'music_mood': row['music_mood'],
		'count': row['count'], 'require_approval': bool(row['require_approval']),
		'created_by': 'scheduler',
	}
	cmd = [sys.executable, '-m', 'pipeline.runner', '--job-json', json.dumps(job_dict, ensure_ascii=False)]
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	logdir = os.path.join(ROOT, 'logs')
	os.makedirs(logdir, exist_ok=True)
	log = os.path.join(logdir, 'runner' + job_id + '.log')
	f = open(log, 'a', encoding='utf-8')
	p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	c.execute('UPDATE jobs SET status=?, error=? WHERE id=?', ('running', 'spawned pid=' + str(p.pid), job_id))
	c.commit()
	return True


def tick():
	import time as tmod
	import os as _os
	_flag = os.path.join(ROOT, 'state', 'paused.flag')
	if os.path.exists(flag):
		print('[scheduler] paused - skip tick')
		return 0
	now = tmod.localtime()
	c = state.connect()
	created = []

	# 1) run_at scheduled jobs (one-shot)
	try:
		rows_at = c.execute('SELECT id FROM jobs WHERE status=? AND run_at IS NOT NULL AND run_at <= ?', ('scheduled', state.now())).fetchall()
	except Exception:
		rows_at = []
	for r in rows_at:
		if dispatch_job(r['id']):
			created.append(r['id'])

	# 2) cron-based channels
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
			jid = 'sch' + str(r['id']) + '' + time.strftime('%Y%m%d%H%M')
			existing = c.execute('SELECT id FROM jobs WHERE id=?', (jid,)).fetchone()
			if existing:
				continue
			c.execute(
				'INSERT INTO jobs (id, channel_id, kind, topic, status, created_at, count, require_approval) VALUES (?,?,?,?,?,?,?,?)',
				(jid, r['id'], sched.get('kind', 'short'), sched.get('topic', ''), 'pending', state.now(), int(sched.get('count', 1)), int(sched.get('require_approval', 0)))
			)
			c.commit()
			created.append(jid)
			dispatch_job(jid)
		except Exception as e:
			print('[scheduler] create job ERR: ' + str(e)[:120])
	return len(created)


def loop_forever(interval=30):
	while True:
		try:
			n = tick()
			if n:
				print('[scheduler] tick created=' + str(n))
		except Exception as e:
			print('[scheduler] tick ERR: ' + str(e)[:200])
		time.sleep(interval)


if __name__ == '__main__':
	loop_forever()
