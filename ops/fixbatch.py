p = 'ops/batch_render.py'
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
b = b.replace(b'FILEMARK', du + b'file' + du)
open(p, 'wb').write(b)
print('fixed')
