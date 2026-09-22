import sqlite3, os, json, sys
DB = os.path.join(os.getcwd(), 'system', 'state.db')
C = sqlite3.connect(DB)
def q(s):
	cur = C.execute(s)
	cols = [d[0] for d in cur.description]
	return [dict(zip(cols, row)) for row in cur.fetchall()]
CMDS = {'latest': lambda: {'channels': q('SELECT name, platform, active, scheduleCron, updatedAt FROM channels ORDER BY name'), 'toolCount': C.execute('SELECT COUNT(*) FROM tools').fetchone()[0], 'changelog': q('SELECT change, createdAt FROM changelog ORDER BY id DESC LIMIT 20')}, 'channels': lambda: q('SELECT * FROM channels ORDER BY name'), 'tools': lambda: q('SELECT name, path, version, updatedAt FROM tools ORDER BY name'), 'doctor': lambda: {'ok': os.path.exists(DB), 'db': DB, 'size': os.path.getsize(DB) if os.path.exists(DB) else 0}}
cmd = sys.argv[1] if len(sys.argv) > 1 else 'latest'
fn = CMDS.get(cmd)
out = fn() if fn else {'error': 'unknown command', 'valid': sorted(CMDS.keys())}
print(json.dumps(out, ensure_ascii=False, indent=2))
