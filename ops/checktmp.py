import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = open('ops/ffmpeg_render.py', encoding='utf-8').read()
for i, l in enumerate(f.split(chr(10)), 1):
	if 'tmp' in l and ('=' in l or 'mkdtemp' in l or '_work' in l):
		print(i, l.strip()[:120])
