import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = open('ops/ffmpeg_render.py', encoding='utf-8').read()
lines = f.split(chr(10))
for i in range(220, 320):
	if i < len(lines) and ('tmp' in lines[i].lower() or 'work' in lines[i].lower()):
		print(i+1, lines[i].strip()[:130])
