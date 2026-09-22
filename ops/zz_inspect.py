import sys
fn = sys.argv[1]
src = open(fn, encoding='utf-8').read()
print('file:', fn)
print('len:', len(src), 'lines:', src.count(chr(10)))
key_main = chr(95) * 2 + 'main' + chr(95) * 2
print('has main:', key_main in src)
key_name = chr(95) * 2 + 'name' + chr(95) * 2
print('has name:', key_name in src)
print('--- last 15 lines ---')
lines = src.split(chr(10))
for i, ln in enumerate(lines[-15:], len(lines) - 14):
	print(i, repr(ln))
