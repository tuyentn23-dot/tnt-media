import sys
p = sys.argv[1]
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
# Fix abspath(file) -> abspath(file)
b = b.replace(b'abspath(file)', b'abspath(' + du + b'file' + du + b')')
b = b.replace(b'def INITMARK', b'def ' + du + b'init' + du)
b = b.replace(b'def REPRMARK', b'def ' + du + b'repr' + du)
b = b.replace(b'== MAINMARK', b'== ' + du + b'main' + du)
open(p, 'wb').write(b)
print('fixed', p, 'len', len(b))
