import io, os
U = chr(95)
D = U + U
Q = chr(39)
files = ['ops/channel_cli.py', 'ops/channel_loader.py', 'ops/channel_style.py', 'ops/channel_pipeline.py', 'ops/multichannel_autopilot.py']
for f in files:
	if not os.path.exists(f):
		continue
	t = io.open(f, encoding='utf-8').read()
	t = t.replace('abspath(file)', 'abspath(' + D + 'file' + D + ')')
	bad = 'if name == ' + Q + 'main' + Q + ':'
	good = 'if ' + D + 'name' + D + ' == ' + Q + D + 'main' + D + Q + ':'
	t = t.replace(bad, good)
	io.open(f, 'w', encoding='utf-8').write(t)
print('DONE')
