import os, sys, io, json, argparse
U = chr(95)
ROOT = os.getcwd()
OUT = os.path.join(ROOT, 'output')
CH = os.path.join(ROOT, 'channels')
MEM = os.path.join(ROOT, 'memory')

def ledgerpaths():
	ps = []
	if os.path.isdir(CH):
		for name in sorted(os.listdir(CH)):
			p = os.path.join(CH, name, 'published' + U + 'ledger.json')
			if os.path.exists(p):
				ps.append(p)
	gp = os.path.join(MEM, 'published' + U + 'ledger.json')
	if os.path.exists(gp):
		ps.append(gp)
	return ps

def publishedfiles():
	files = set()
	for lp in ledgerpaths():
		try:
			d = json.load(io.open(lp, encoding='utf-8'))
		except Exception as e:
			print('[skip]', lp, str(e)[:80])
			continue
		sigs = d.get('signatures', {}) if isinstance(d, dict) else {}
		for k, v in sigs.items():
			if isinstance(v, dict) and v.get('file'):
				files.add(os.path.basename(v['file']))
	return files

def thumbfor(name):
	base = os.path.splitext(name)[0]
	return [base + U + 'thumb.jpg', base + U + 'thumb.png', base + '.jpg']

def clean(force=False):
	files = publishedfiles()
	cand = []
	for name in files:
		mp4 = os.path.join(OUT, name)
		if os.path.exists(mp4):
			cand.append(mp4)
		for th in thumbfor(name):
			tp = os.path.join(OUT, th)
			if os.path.exists(tp):
				cand.append(tp)
	print('[clean] published:', len(files), 'candidates:', len(cand))
	for p in cand[:15]:
		print(' -', os.path.basename(p))
	if not force:
		print('[clean] DRY-RUN. Dung --force de xoa that.')
		return {'mode': 'dry-run', 'would': len(cand)}
	n = 0
	for p in cand:
		try:
			os.remove(p)
			n = n + 1
		except Exception as e:
			print('[err]', p, str(e)[:80])
	print('[clean] deleted:', n)
	return {'mode': 'force', 'deleted': n}

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('--force', action='store_true')
	args = ap.parse_args()
	print(clean(force=args.force))
	return 0

if sys.argv[0].endswith('publish_cleanup.py'):
	sys.exit(main())
