import io, os
U = chr(95)
D = U + U + 'file' + U + U
bad = 'abspath' + '(' + 'file' + ')'
good = 'abspath' + '(' + D + ')'
files = ['ops/channel_loader.py', 'ops/channel_style.py', 'ops/channel_pipeline.py', 'ops/multichannel_autopilot.py', 'ops/channel_cli.py']
for f in files:
	if not os.path.exists(f):
		continue
	t = io.open(f, encoding='utf-8').read()
	t2 = t.replace(bad, good)
	if t2 != t:
		io.open(f, 'w', encoding='utf-8').write(t2)
		print('FIXED', f)
	else:
		print('OK', f)
