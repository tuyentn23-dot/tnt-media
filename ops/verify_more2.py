import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from pipeline import state
c = state.connect()
n = c.execute("SELECT COUNT(*) FROM jobs WHERE status='pending_approval'").fetchone()[0]
print('jobs pending_approval:', n)
s = open('app/server.py', encoding='utf-8').read()
lines = s.split(chr(10))
for i, l in enumerate(lines):
	if 'backup' in l.lower() and ('def ' in l or '@app' in l or 'copy' in l):
		print('server.py', i+1, l.strip()[:100])
if os.path.exists('ops/start.py'):
	s2 = open('ops/start.py', encoding='utf-8').read()
	print('start.py has youtube_url:', 'youtube_url' in s2)
	print('start.py has youtube_id:', 'youtube_id' in s2)
s3 = open('app/tray.py', encoding='utf-8').read()
print('tray disables ALL channels on pause:', 'UPDATE channels SET enabled=0' in s3)
