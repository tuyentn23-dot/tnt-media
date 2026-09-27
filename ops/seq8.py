import os, sys, time, json, subprocess
sys.path.insert(0, os.getcwd())
U = chr(95)
JOBS = open('logs/' + U + 'batch8.txt').read().strip().split(chr(10))
for jid in JOBS:
	print('=== ' + jid + ' ===', flush=True)
	from pipeline import state
	c = state.connect()
	r = c.execute('SELECT channel' + U + 'id, kind FROM jobs WHERE id=?', (jid,)).fetchone()
	if not r:
		print('MISS', jid, flush=True)
		continue
	cid, kind = r[0], r[1]
	cmd = [sys.executable, '-m', 'pipeline.runner', '--channel', cid]
	if kind:
		cmd += ['--kind', kind]
	print('cmd:', ' '.join(cmd), flush=True)
	log = open('logs/seq' + jid + '.log', 'w')
	proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
	proc.wait()
	log.close()
	print('done', jid, flush=True)
	time.sleep(5)
print('ALL DONE', flush=True)
