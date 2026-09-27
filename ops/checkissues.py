import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
# 1. route publish trong server.py
s = open('app/server.py', encoding='utf-8').read()
print('=== server.py publish routes ===')
for i, l in enumerate(s.split(chr(10)), 1):
	if 'publish' in l and ('@app' in l or 'def ' in l):
		print(i, l)
print()
print('=== ffmpeg_render temp files ===')
f = open('ops/ffmpeg_render.py', encoding='utf-8').read()
for i, l in enumerate(f.split(chr(10)), 1):
	if '_work' in l or "c0.txt" in l or 'hook.txt' in l or 'tmp' in l.lower():
		print(i, l.strip()[:100])
