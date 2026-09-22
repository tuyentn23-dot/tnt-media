import io
for f in ['ops/channel_style.py', 'ops/channel_pipeline.py', 'ops/multichannel_autopilot.py', 'ops/channel_cli.py']:
	t = io.open(f, encoding='utf-8').read()
	lines = t.splitlines()
	print('===', f)
	for l in lines[-4:]:
		print(' ', repr(l))
