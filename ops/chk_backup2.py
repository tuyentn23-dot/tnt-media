src = open('app/server.py', 'rb').read()
NL = bytes([13, 10])
TB = bytes([9])
old = (
 b"@app.post('/api/backup')" + NL
 + b'def backup():' + NL
 + TB + b'import shutil' + NL
 + TB + b"bk = os.path.join(ROOT, 'state', 'backup')" + NL
 + TB + b'os.makedirs(bk, exist_ok=True)' + NL
 + TB + b"dst = os.path.join(bk, 'pipeline' + time.strftime('%Y%m%d_%H%M%S') + '.db')" + NL
 + TB + b'try:' + NL
 + TB + TB + b'shutil.copy2(state.DB, dst)' + NL
 + TB + TB + b"return {'ok': True, 'file': os.path.basename(dst)}" + NL
 + TB + b'except Exception as e:' + NL
 + TB + TB + b"return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)" + NL
)
print('old bytes in src:', old in src)
if old not in src:
 i = src.find(b"@app.post('/api/backup')")
 print('actual:', repr(src[i:i+len(old)]))
