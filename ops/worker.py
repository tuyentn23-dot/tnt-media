import sqlite3, os, random
from datetime import datetime
DB = os.path.join(os.getcwd(), 'system', 'state.db')
C = sqlite3.connect(DB)
cols = lambda cur: [d[0] for d in cur.description]
rows = lambda cur: [dict(zip(cols(cur), r)) for r in cur.fetchall()]
now = datetime.now().isoformat(timespec='seconds')
Q = 'queued'
D = 'done'
pending = rows(C.execute('SELECT id, channelId FROM jobs WHERE status = ? ORDER BY id LIMIT 5', (Q,)))
print('PENDING:', len(pending))
TP = {'Mialinhcute': ['kitten dance', 'anime chibi', 'roblox obby', 'gacha story'], 'vilevi5676': ['5 foods', 'why cats purr', 'lifehack', '90s toys']}
FM = ['shorts_fact', 'shorts_top5', 'shorts_story', 'shorts_quiz']
nameOf = lambda chId: C.execute('SELECT name FROM channels WHERE id = ?', (chId,)).fetchone()[0]
make = lambda j: (j['channelId'], random.choice(TP.get(nameOf(j['channelId']), ['misc'])), random.choice(FM))
decs = [(a, b, c, 'Hook ' + b, random.uniform(0.5, 0.9), 'v1', now) for (a, b, c) in [make(j) for j in pending]]
C.executemany('INSERT INTO decisions (channelId, topic, format, hook, score, rationale, chosenAt) VALUES (?, ?, ?, ?, ?, ?, ?)', decs)
C.commit()
decIds = rows(C.execute('SELECT id FROM decisions ORDER BY id DESC LIMIT ?', (len(decs),)))[::-1]
vids = [(pending[i]['channelId'], decIds[i]['id'], 'output/v_' + str(decIds[i]['id']) + '.mp4', 'queued_render', 'local') for i in range(len(decs))]
C.executemany('INSERT INTO videos (channelId, decisionId, path, status, renderWorker) VALUES (?, ?, ?, ?, ?)', vids)
C.executemany('UPDATE jobs SET status = ?, finishedAt = ? WHERE id = ?', [(D, now, j['id']) for j in pending])
C.commit()
print('decisions:', len(decs))
print('videos:', len(vids))
C.close()
