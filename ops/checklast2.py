import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from pipeline import state
c = state.connect()
rows = c.execute('SELECT id, channel_id, youtube_id, title, status FROM publications WHERE id IN (145,146)').fetchall()
for r in rows:
	print(r['id'], r['channel_id'], r['status'], r['youtube_id'], (r['title'] or '')[:50])
