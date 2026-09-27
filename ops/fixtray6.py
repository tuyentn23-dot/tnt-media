p = 'app/tray.py'
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
b = b.replace(b'if name ==', b'if ' + du + b'name' + du + b' ==')
open(p, 'wb').write(b)
print('fixed')
