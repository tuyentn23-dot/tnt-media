import sys
p = sys.argv[1]
b = open(p, 'rb').read()
u = bytes([95])
du = u + u
for name in (b'init', b'repr', b'main', b'file', b'name', b'class', b'dict', b'str', b'del'):
	b = b.replace(b'def ' + name.upper() + b'MARK', b'def ' + du + name + du)
	b = b.replace(b'== ' + name.upper() + b'MARK', b'== ' + du + name + du)
	b = b.replace(b'FILEMARK', du + b'file' + du)
	b = b.replace(b'NAMEMARK', du + b'name' + du)
	b = b.replace(b'CLASSMARK', du + b'class' + du)
open(p, 'wb').write(b)
print('patched', p, 'len', len(b))
