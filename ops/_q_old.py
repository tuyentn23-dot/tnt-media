import sqlite3
c = sqlite3.connect('state/pipeline.db')
c.row_factory = sqlite3.Row
rows = c.execute(
 'SELECT id, channel_id, kind, topic, created_at FROM jobs WHERE status=? ORDER BY created_at',
 ('pending_approval',)
).fetchall()
for r in rows:
 print(r['id'], '|', r['channel_id'], '|', r['kind'], '|', r['created_at'])
