p = 'pipeline/runner.py'
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
b = b.replace(b'abspath(file)', b'abspath(' + du + b'file' + du + b')')
b = b.replace(b'if name ==', b'if ' + du + b'name' + du + b' ==')
b = b.replace(b'== MAINMARK', b'== ' + bytes([39]) + du + b'main' + du + bytes([39]))
open(p, 'wb').write(b)
print('fixed runner')
