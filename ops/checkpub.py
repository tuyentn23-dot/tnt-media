import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from pipeline import state
c = state.connect()
rows = c.execute("SELECT id, channel_id, status, youtube_id, title, file_path FROM publications WHERE signature LIKE 'pub_%' ORDER BY id").fetchall()
print('total:', len(rows))
for r in rows:
	print(r['id'], r['channel_id'], r['status'], r['youtube_id'] or '-', (r['title'] or '')[:40])
