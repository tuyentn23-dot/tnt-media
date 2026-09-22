import sqlite3, os, json
DB = os.path.join(os.getcwd(), 'system', 'state.db')
c = sqlite3.connect(DB)
print('channels:')
for r in c.execute('SELECT name, platform, active, scheduleCron, updatedAt FROM channels ORDER BY name').fetchall():
 print(r)
print('tools count:', c.execute('SELECT COUNT(*) FROM tools').fetchone()[0])
print('changelog last 3:')
for r in c.execute('SELECT change, createdAt FROM changelog ORDER BY id DESC LIMIT 3').fetchall():
 print(r)
c.close()
