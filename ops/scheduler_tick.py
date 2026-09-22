import sqlite3, os, json
from datetime import datetime, timedelta
DB = os.path.join(os.getcwd(), 'system', 'state.db')
C = sqlite3.connect(DB)
cols = lambda cur: [d[0] for d in cur.description]
rows = lambda cur: [dict(zip(cols(cur), r)) for r in cur.fetchall()]
C.execute('CREATE TABLE IF NOT EXISTS schedule (channel TEXT PRIMARY KEY, intervalMinutes INTEGER DEFAULT 360, nextRunAt TEXT, lastRunAt TEXT)')
now = datetime.now().isoformat(timespec='seconds')
active = rows(C.execute('SELECT name FROM channels WHERE active = 1'))
existing = set(r['channel'] for r in rows(C.execute('SELECT channel FROM schedule')))
new = [(c['name'], 360, now) for c in active if c['name'] not in existing]
C.executemany('INSERT INTO schedule (channel, intervalMinutes, nextRunAt) VALUES (?, ?, ?)', new)
C.commit()
due = rows(C.execute('SELECT channel, nextRunAt FROM schedule WHERE nextRunAt <= ?', (now,)))
print('NOW:', now)
print('NEW CHANNELS:', len(new))
print('DUE:', len(due))
C.executemany('INSERT INTO jobs (channelId, kind, payloadJson, status, scheduledFor) VALUES ((SELECT id FROM channels WHERE name = ?), ?, ?, ?, ?)', [(d['channel'], 'publish', json.dumps({'channel': d['channel']}), 'queued', d['nextRunAt']) for d in due])
nxtTime = (datetime.now() + timedelta(minutes=360)).isoformat(timespec='seconds')
C.executemany('UPDATE schedule SET nextRunAt = ?, lastRunAt = ? WHERE channel = ?', [(nxtTime, now, d['channel']) for d in due])
C.commit()
print('queued total:', C.execute('SELECT COUNT(*) FROM jobs WHERE status = "queued"').fetchone()[0])
C.close()
