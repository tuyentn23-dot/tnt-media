import sqlite3, os, json, hashlib
from datetime import datetime
ROOT = os.getcwd()
DB = os.path.join(ROOT, 'system', 'state.db')
SCHEMA = os.path.join(ROOT, 'system', 'schema.sql')
OPS = os.path.join(ROOT, 'ops')
CH = os.path.join(ROOT, 'channels')
now = lambda: datetime.now().isoformat(timespec='seconds')
hashFile = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12]
con = sqlite3.connect(DB)
con.executescript(open(SCHEMA, encoding='utf-8').read())
cur = con.cursor()
pyFiles = sorted(n for n in os.listdir(OPS) if n.endswith('.py')) if os.path.isdir(OPS) else []
rows = [(n, 'ops/' + n, str(os.path.getsize(os.path.join(OPS, n))), hashFile(os.path.join(OPS, n)), now()) for n in pyFiles]
cur.executemany('INSERT INTO tools (name, path, version, description, updatedAt) VALUES (?, ?, ?, ?, ?) ON CONFLICT(name) DO UPDATE SET path=excluded.path, version=excluded.version, description=excluded.description, updatedAt=excluded.updatedAt', rows)
toolCount = cur.execute('SELECT COUNT() FROM tools').fetchone()[0]
chFiles = sorted(n for n in os.listdir(CH) if n.endswith('.json') and not n.startswith('_') and n != 'channel_template.json') if os.path.isdir(CH) else []
data = [json.load(open(os.path.join(CH, n), encoding='utf-8')) for n in chFiles]
chRows = [(d.get('name', n[:-5]), d.get('platform', 'youtube'), d.get('tokenPath', ''), 1 if d.get('active') else 0, json.dumps(d, ensure_ascii=False), d.get('scheduleCron', ''), now(), now()) for d, n in zip(data, chFiles)]
cur.executemany('INSERT INTO channels (name, platform, tokenPath, active, styleJson, scheduleCron, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(name) DO UPDATE SET platform=excluded.platform, tokenPath=excluded.tokenPath, active=excluded.active, styleJson=excluded.styleJson, scheduleCron=excluded.scheduleCron, updatedAt=excluded.updatedAt', chRows)
chCount = cur.execute('SELECT COUNT() FROM channels').fetchone()[0]
cur.execute('INSERT INTO changelog (version, entity, change, actor) VALUES (?, ?, ?, ?)', ('v1', 'state_sync', 'synced tools=' + str(toolCount) + ' channels=' + str(chCount), 'agent'))
con.commit()
print('DB:', DB)
print('tools:', toolCount)
print('channels:', chCount)
con.close()

try:
    import runpy
    runpy.run_path(os.path.join(OPS, 'sync_a_to_b.py'), run_name='__main__')
except Exception as _e:
    print('A->B skip:', _e)
