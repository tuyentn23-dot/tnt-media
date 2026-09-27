# -- coding: utf-8 --
import subprocess, sys, os, time
NL = chr(10)
PY = sys.executable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JOBS = [
	('Mialinhcute', 'cute_animals', 'cute_new_01'),
	('Mialinhcute', 'meme', 'meme_new_01'),
	('vilevi5676', 'whatif', 'whatif_new_01'),
	('vilevi5676', 'facts', 'facts_new_01'),
	('vilevi5676', 'curiosity', 'curio_new_01'),
	('vilevi5676', 'food', 'food_new_01'),
]

os.chdir(ROOT)
logdir = os.path.join(ROOT, 'logs')
os.makedirs(logdir, exist_ok=True)

for cid, kind, iid in JOBS:
	log = os.path.join(logdir, 'batch_' + cid + '_' + kind + '.log')
	cmd = [PY, '-m', 'pipeline.runner', '--channel', cid, '--kind', kind, '--item-id', iid]
	with open(log, 'w', encoding='utf-8') as lf:
		p = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, cwd=ROOT)
		rc = p.wait()
	print(cid, kind, iid, 'rc=', rc)
print('ALL DONE')
