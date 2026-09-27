import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = open('logs/_publish_public.log', encoding='utf-16', errors='replace').read()
out = []
for line in d.split(chr(10)):
	if 'youtube_id' in line or line.startswith('---') or 'DONE' in line or 'FAIL' in line:
		out.append(line.strip()[:180])
open('logs/_publish_summary.txt', 'w', encoding='utf-8').write(chr(10).join(out))
print('wrote', len(out))
