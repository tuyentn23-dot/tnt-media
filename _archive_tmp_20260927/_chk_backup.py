src = open('app/server.py', 'rb').read()
CR = bytes([13])
LF = bytes([10])
print('CR:', src.count(CR))
print('LF:', src.count(LF))
NL = bytes([10])
key = b"@app.post('/api/backup')"
i = src.find(key)
print(repr(src[i:i+400]))
