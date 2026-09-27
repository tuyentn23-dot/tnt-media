import sys
p = sys.argv[1]
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
b = b.replace(b'if name == ' + du + b'main' + du, b'if ' + du + b'name' + du + b' == ' + du + b'main' + du)
open(p, 'wb').write(b)
print('fixed', p)
