src = open('app/server.py', 'rb').read()
key = b"@app.post('/api/backup')"
i = src.find(key)
# find next decorator
j = src.find(b'@app.', i + len(key))
print('segment length:', j - i)
print('ACTUAL FULL:')
print(repr(src[i:j]))
