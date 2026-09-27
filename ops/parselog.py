import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = open('logs/_publish_public.log', encoding='utf-16', errors='replace').read()
for line in d.split(chr(10)):
	if 'youtube_id' in line or line.startswith('---') or 'DONE' in line or 'FAIL' in line:
		print(line.strip()[:160])
