# -- coding: utf-8 --
# guardian/integrity.py - Verify SHA256 critical files
import os, sys, json, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'guardian', 'critical.sha256.json')

def sha256(path):
	h = hashlib.sha256()
	with open(path, 'rb') as f:
		for chunk in iter(lambda: f.read(65536), b''):
			h.update(chunk)
	return h.hexdigest()

def verify():
	if not os.path.exists(MANIFEST):
		return {'ok': False, 'err': 'manifest missing'}
	m = json.load(open(MANIFEST, encoding='utf-8'))
	files = m.get('files', {})
	bad = []
	missing = []
	for f, expected in files.items():
		p = os.path.join(ROOT, f)
		if not os.path.exists(p):
			missing.append(f)
			continue
		if expected is None:
			continue
		actual = sha256(p)
		if actual != expected:
			bad.append(f)
	ok = not bad and not missing
	return {'ok': ok, 'bad': bad, 'missing': missing, 'total': len(files)}

def snapshot():
	manifest = {}
	d = json.load(open(os.path.join(ROOT, 'guardian', 'critical.json'), encoding='utf-8'))
	for group, files in d.items():
		for f in files:
			p = os.path.join(ROOT, f)
			manifest[f] = sha256(p) if os.path.exists(p) else None
	import datetime
	out = {'version': 1, 'generated': datetime.datetime.now().isoformat(), 'files': manifest}
	open(MANIFEST, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=2))
	return len(manifest)



def verify_manifest_git():
	import subprocess
	try:
		r = subprocess.run(
			['git', 'show', 'HEAD:guardian/critical.sha256.json'],
			capture_output=True, text=True, cwd=ROOT
		)
		if r.returncode != 0:
			return {'ok': True, 'note': 'no git version yet'}
		committed = r.stdout
		current = open(MANIFEST, encoding='utf-8').read()
		if committed.strip() != current.strip():
			return {'ok': False, 'err': 'manifest modified vs git HEAD'}
		return {'ok': True}
	except Exception as e:
		return {'ok': False, 'err': str(e)[:80]}

def main():
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == 'snapshot':
		n = snapshot()
		print('Snapshot: ' + str(n) + ' files')
		sys.exit(0)
	mr = verify_manifest_git()
	if not mr.get('ok'):
		print('MANIFEST COMPROMISED:', mr.get('err'))
		sys.exit(1)
	r = verify()
	if r['ok']:
		print('INTEGRITY OK - ' + str(r['total']) + ' files')
		sys.exit(0)
	print('INTEGRITY FAIL')
	for f in r.get('bad', []):
		print(' MODIFIED: ' + f)
	for f in r.get('missing', []):
		print(' MISSING: ' + f)
	sys.exit(1)

if __name__ == '__main__':
	main()