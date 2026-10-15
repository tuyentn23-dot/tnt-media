# tool: gacha-anime
# -- coding: utf-8 --
# modules/render/gacha.py - Render video gacha anime
import os, sys
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'gacha-anime',
	'name': 'render.gacha',
	'version': '1.0.0',
	'interface': 'create(prompt, out_path, wait=240) -> dict',
	'deps': ['ops.gacha_worker']
}


def log(m):
	try:
		print('[gacha] ' + str(m), flush=True)
	except Exception:
		pass


def create(prompt, out_path, wait=240, aspect=None):
	import subprocess, json
	worker = os.path.join(ROOT, 'ops', 'gacha_worker.py')
	if not os.path.exists(worker):
		return {'ok': False, 'error': 'gacha_worker.py missing'}
	item = {'topic': prompt[:80], 'hook': prompt[:100], 'body': prompt}
	payload = {'item': item, 'out': out_path}
	cmd = [sys.executable, worker, '--json', json.dumps(payload, ensure_ascii=False)]
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	log_p = os.path.join(ROOT, 'logs', 'gacha_worker.log')
	os.makedirs(os.path.dirname(log_p), exist_ok=True)
	try:
		f = open(log_p, 'a', encoding='utf-8')
		f.write(chr(10) + chr(61) * 40 + chr(10))
		f.flush()
		proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	except Exception as e:
		return {'ok': False, 'error': 'spawn fail: ' + str(e)[:200]}
	hard = wait + 120
	try:
		proc.wait(timeout=hard)
	except subprocess.TimeoutExpired:
		try:
			proc.kill()
		except Exception:
			pass
		return {'ok': False, 'error': 'gacha timeout ' + str(hard) + 's'}
	if proc.returncode != 0:
		return {'ok': False, 'error': 'gacha exit ' + str(proc.returncode)}
	if os.path.exists(out_path):
		return {'ok': True, 'path': out_path, 'engine': 'gacha'}
	return {'ok': False, 'error': 'gacha no file'}


def health():
	return {'ok': os.path.exists(os.path.join(ROOT, 'ops', 'gacha_worker.py'))}
