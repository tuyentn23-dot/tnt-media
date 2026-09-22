import os
L = []
A = L.append
A('import os, json, sqlite3')
A('from http.server import HTTPServer, BaseHTTPRequestHandler')
A('from urllib.parse import urlparse')
A('ROOT = os.getcwd()')
A('DB = os.path.join(ROOT, 'system', 'state.db')')
A('PORT = 8765')
A('def q(sql, args=()):')
A('	con = sqlite3.connect(DB)')
A('	con.rowFactory = sqlite3.Row')
A('	rows = [dict(r) for r in con.execute(sql, args).fetchall()]')
A('	con.close()')
A('	return rows')
A('def stateLatest():')
A('	return {')
A('		"channels": q("SELECT name, platform, active, scheduleCron, updatedAt FROM channels ORDER BY name"),')
A('		"toolCount": q("SELECT COUNT(*) AS n FROM tools")[0]["n