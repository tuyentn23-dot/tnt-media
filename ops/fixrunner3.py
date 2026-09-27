p = 'pipeline/runner.py'
b = open(p, 'rb').read()
u = bytes([95])
b = b.replace(b'def call(', b'def ' + u + b'call(')
open(p, 'wb').write(b)
print('fixed _call')
