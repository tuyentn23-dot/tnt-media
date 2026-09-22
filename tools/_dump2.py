import io
out = []
for f in ['ops/channel_style.py', 'ops/channel_pipeline.py', 'ops/multichannel_autopilot.py', 'ops/channel_cli.py']:
	t = io.open(f, encoding='utf-8').read()
	lines = t.splitlines()
	out.append('=== ' + f + ' lines=' + str(len(lines)))
	for l in lines[-4:]:
		out.append(' ' + repr(l))
io.open('tools/_dump.txt', 'w', encoding='utf-8').write(chr(10).join(out))
