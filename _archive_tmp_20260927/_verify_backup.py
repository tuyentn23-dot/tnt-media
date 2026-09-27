import sqlite3, sys
p = sys.argv[1]
c = sqlite3.connect(p)
rows = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('tables:', [r[0] for r in rows])
for t in ('jobs','publications','channels','audit','assets'):
 try:
 n = c.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
 print(t, n)
 except Exception as e:
 print(t, 'ERR', str(e)[:80])
c.close()
