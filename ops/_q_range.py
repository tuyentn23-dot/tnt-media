import sqlite3
c = sqlite3.connect('state/pipeline.db')
c.row_factory = sqlite3.Row
rows = c.execute(
 "SELECT MIN(created_at) AS mn, MAX(created_at) AS mx FROM jobs WHERE status='pending_approval'"
).fetchall()
for r in rows:
 print('range:', r['mn'], '->', r['mx'])

rows2 = c.execute(
 "SELECT id, channel_id, kind, created_at FROM jobs WHERE status='pending_approval' ORDER BY created_at"
).fetchall()
print('TOTAL:', len(rows2))
for r in rows2[:10]:
 print(r['id'], '|', r['channel_id'], '|', r['kind'], '|', r['created_at'])
print('...')
for r in rows2[-5:]:
 print(r['id'], '|', r['channel_id'], '|', r['kind'], '|', r['created_at'])
