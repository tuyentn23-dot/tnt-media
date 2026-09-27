import os, sqlite3
c = sqlite3.connect('state/pipeline.db')
c.row_factory = sqlite3.Row
Q = chr(39)
rows = c.execute(
 'SELECT id, channel_id, kind, topic, created_at FROM jobs WHERE status=? ORDER BY created_at LIMIT 15',
 ('pending_approval',)
).fetchall()
for r in rows:
 print(dict(r))
print('---')
rows2 = c.execute(
 'SELECT id, channel_id, kind, topic, created_at FROM jobs WHERE status=? ORDER BY created_at',
 ('pending_approval',)
).fetchall()
print('TOTAL pending_approval:', len(rows2))
