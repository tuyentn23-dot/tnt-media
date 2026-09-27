import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = open('ops/ffmpeg_render.py', encoding='utf-8').read()
lines = f.split(chr(10))
for i, l in enumerate(lines):
	if 'tmp =' in l or 'tmp=' in l or 'mkdtemp' in l or '_work' in l:
		print(i+1, l.strip()[:130])
