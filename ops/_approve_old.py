import sqlite3
c = sqlite3.connect('state/pipeline.db')
c.row_factory = sqlite3.Row

# Dem so job pending_approval cũ hơn 2026-09-26 00:00
rows = c.execute(
 "SELECT id FROM jobs WHERE status='pending_approval' AND created_at < '2026-09-26'"
).fetchall()
print('old (< 2026-09-26):', len(rows))

# Dem recent
rows2 = c.execute(
 "SELECT id FROM jobs WHERE status='pending_approval' AND created_at >= '2026-09-26'"
).fetchall()
print('recent (>= 2026-09-26):', len(rows2))

# Mark tat ca old pending_approval -> cancelled
ids = [r['id'] for r in rows]
if ids:
 q = 'UPDATE jobs SET status=? WHERE id IN (' + ','.join('?'*len(ids)) + ')'
 c.execute(q, ['cancelled'] + ids)
 c.commit()
 print('Marked cancelled:', len(ids))

# Verify
rows3 = c.execute("SELECT status, COUNT(1) AS n FROM jobs GROUP BY status").fetchall()
print('After:')
for r in rows3:
 print(' ', r['status'], '=', r['n'])
