import os, sys, platform, shutil
print('python:', sys.version.split()[0])
print('platform:', platform.platform())
print('machine:', platform.machine())
t = shutil.disk_usage('.')
print('disk free GB:', round(t.free / 1e9, 1))
for fn in ['.env', '.env.example']:
	if not os.path.exists(fn):
		continue
	print('---', fn)
	txt = open(fn, encoding='utf-8').read()
	for ln in txt.split(chr(10)):
		ln = ln.strip()
		if not ln or ln.startswith(chr(35)):
			continue
		if chr(61) in ln:
			k, v = ln.split(chr(61), 1)
			vs = (v[:8] + '...') if len(v) > 12 else v
			print(' ', k.strip(), '=', vs)