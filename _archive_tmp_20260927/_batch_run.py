import os, sys, time, json, subprocess
sys.path.insert(0, os.getcwd())
from pipeline import state
JOBS = ["job_20260926_072116", "job_20260926_072440", "job_20260926_072443", "job_20260926_072446", "job_20260926_072449", "job_20260926_072452", "job_20260926_072455", "job_20260926_072458"]
for jid in JOBS:
	c = state.connect()
	r = c.execute('SELECT channel_id, kind FROM jobs WHERE id=?', (jid,)).fetchone()
	if not r:
		print('MISS', jid)
		continue
	cid, kind = r[0], r[1]
	print('=== ', jid, cid, kind, flush=True)
	cmd = [sys.executable, '-m', 'pipeline.runner', '--channel', cid]
	if kind:
		cmd += ['--kind', kind]
	log = open('logs/seq' + jid + '.log', 'w')
	proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
	proc.wait()
	log.close()
	print('done ', jid, flush=True)
	time.sleep(3)
