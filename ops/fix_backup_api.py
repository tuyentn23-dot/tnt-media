import ast
NL = bytes([13, 10])
TB = bytes([9])
p = 'app/server.py'
src = open(p, 'rb').read()
key = b"@app.post('/api/backup')"
i = src.find(key)
# find next decorator after this
j = src.find(b'@app.', i + len(key))
assert i >= 0 and j > i
print('segment length:', j - i)

new = (
 b"@app.post('/api/backup')" + NL
 + b'def backup():' + NL
 + TB + b'from ops import backup_state as _bs' + NL
 + TB + b"bk = os.path.join(ROOT, 'state', 'backup')" + NL
 + TB + b'try:' + NL
 + TB + TB + b'dst = _bs.backup_sqlite(state.DB, bk)' + NL
 + TB + TB + b"return {'ok': True, 'file': os.path.basename(dst), 'bytes': os.path.getsize(dst)}" + NL
 + TB + b'except Exception as e:' + NL
 + TB + TB + b"return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)" + NL
 + NL
)

out = src[:i] + new + src[j:]
open(p, 'wb').write(out)
print('PATCHED')
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
