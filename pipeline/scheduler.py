# -- coding: utf-8 --
# pipeline/scheduler.py - Scheduler nhe (thread + DB + worker dispatch)
import os, sys, time, threading, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state


def parse_cron(expr):
	p = (expr or '').split()
	if len(p) != 5:
		return None
	out = {'minute': set(), 'hour': set()}
	def expand(field, lo, hi):
		if field == '*': return set(range(lo, hi+1))
		s = set()
		for part in field.split(','):
			if '-' in part:
				a, b = part.split('-', 1)
				s.update(range(int(a), int(b)+1))
			else:
				s.add(int(part))
		return s
	try:
		out['minute'] = expand(p[0], 0, 59)
		out['hour'] = expand(p[1], 0, 23)
	except Exception:
		return None
	return out


def due_now(cron, now):
	c = parse_cron(cron)
	if not c: return False
	return (now.tm_min in c['minute'] and now.tm_hour in c['hour'])


def dispatch_job(job_id):
	"""Spawn runner cho job nay o tien trinh rieng, log vao logs/."""
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
	log = os.path.join(logdir, 'runner_' + job_id + '.log')
	f = open(log, 'a', encoding='utf-8')
	p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	c.execute('UPDATE jobs SET status=?, error=? WHERE id=?', ('running', 'spawned pid=' + str(p.pid), job_id))
	c.commit()
	return True


def tick():
	import time as tmod
	import os as _os
	_flag = _os.path.join(ROOT, 'state', 'paused.flag')
	if _os.path.exists(_flag):
		print('[scheduler] paused - skip tick')
		return 0
	now = tmod.localtime()
	c = state.connect()
	rows = c.execute('SELECT id, schedule FROM channels WHERE enabled=1').fetchall()
	n = 0
	created = []
	for r in rows:
		try:
			sched = json.loads(r['schedule'] or '{}')
		except Exception:
			sched = {}
		cron = sched.get('cron') or sched.get('scheduleCron') or ''
		if not due_now(cron, now):
			continue
		jid = 'sch_' + r['id'] + '' + tmod.strftime('%Y%m%d%H%M', now)
		res = c.execute('INSERT OR IGNORE INTO jobs (id, channel_id, status, priority, created_by, created_at, updated_at) VALUES (?,?,?,?,?,?,?)', (jid, r['id'], 'pending', 7, 'scheduler', state.now(), state.now()))
		if res.rowcount > 0:
			n += 1
			created.append(jid)
	c.commit()
	for jid in created:
		try:
			dispatch_job(jid)
			time.sleep(1)
		except Exception as e:
			print('[scheduler] dispatch FAIL ' + jid + ': ' + str(e)[:120])
	return n


def run(interval=60, stop_event=None):
	print('[scheduler] start, tick ' + str(interval) + 's')
	while True:
		if stop_event and stop_event.is_set():
			break
		try:
			n = tick()
			if n:
				print('[scheduler] created+dispatched ' + str(n) + ' jobs')
		except Exception as e:
			print('[scheduler] ERR: ' + str(e)[:120])
		time.sleep(interval)


if __name__ == '__main__':
	run()
