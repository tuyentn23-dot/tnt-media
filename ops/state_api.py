import os, json, sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
ROOT = os.getcwd()
DB = os.path.join(ROOT, 'system', 'state.db')
PORT = 8765
U = chr(95)
def q(s, a=()):
 c = sqlite3.connect(DB); c.rowFactory = sqlite3.Row; r = [dict(x) for x in c.execute(s, a).fetchall()]; c.close(); return r
def sLatest(): return {'channels': q('SELECT name, platform, active, scheduleCron, updatedAt FROM channels ORDER BY name'), 'toolCount': q('SELECT COUNT(*) AS n FROM tools')[0]['n'], 'changelog': q('SELECT change, createdAt FROM changelog ORDER BY id DESC LIMIT 20')}
def sChannels(): return q('SELECT * FROM channels ORDER BY name')
def sTools(): return q('SELECT name, path, version, updatedAt FROM tools ORDER BY name')
def sDoctor(): return {'ok': os.path.exists(DB), 'db': DB}
ROUTES = {'/': lambda: {'ok': True, 'service': 'tnt-media-state-api'}, '/health': lambda: {'ok': True}, '/state/latest': sLatest, '/channels': sChannels, '/tools': sTools, '/doctor': sDoctor}
def doGET(self):
 p = urlparse(self.path).path; fn = ROUTES.get(p); self.sendJson(fn() if fn else {'error': 'not found', 'path': p}, 200 if fn else 404)
def sendJson(self, o, code=200):
 b = json.dumps(o, ensure_ascii=False, indent=2).encode('utf-8'); self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
def logMsg(self, *a): pass
methods = {'do' + U + 'GET': doGET, 'sendJson': sendJson, 'log' + U + 'message': logMsg}
H = type('H', (BaseHTTPRequestHandler,), methods)
print('TNT Media State API on http://127.0.0.1:' + str(PORT))
HTTPServer(('127.0.0.1', PORT), H).serve_forever()
