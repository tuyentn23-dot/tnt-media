import io, os
U = chr(95)
Q = chr(39)
D = U + U
files = ['ops/channel_loader.py', 'ops/channel_style.py', 'ops/channel_pipeline.py', 'ops/multichannel_autopilot.py', 'ops/channel_cli.py']
for f in files:
	if not os.path.exists(f):
		continue
	t = io.open(f, encoding='utf-8').read()
	bad1 = 'if name == ' + Q + 'main' + Q + ':'
	good = 'if ' + D + 'name' + D + ' == ' + Q + D + 'main' + D + Q + ':'
	t = t.replace(bad1, good)
	io.open(f, 'w', encoding='utf-8').write(t)
	print('OK', f, 'contains_main_guard=', good in t)
