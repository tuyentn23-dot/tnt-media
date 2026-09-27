import sys
p = 'app/tray.py'
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
q = bytes([39])
b = b.replace(b'FILEMARK', du + b'file' + du)
b = b.replace(b'== MAINMARK', b'== ' + q + du + b'main' + du + q)
open(p, 'wb').write(b)
print('fixed tray')
