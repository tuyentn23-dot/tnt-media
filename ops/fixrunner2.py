p = 'pipeline/runner.py'
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
q = bytes([39])
b = b.replace(b'== ' + du + b'main' + du + b':', b'== ' + q + du + b'main' + du + q + b':')
open(p, 'wb').write(b)
print('fixed')
