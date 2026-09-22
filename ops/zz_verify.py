# verify.py - kiem tra syntax + tim name
import ast, sys
fn = sys.argv[1] if len(sys.argv) > 1 else 'ops/gacha_anime_parts.py'
src = open(fn, encoding='utf-8').read()
print('file:', fn)
print('len:', len(src), 'lines:', src.count(chr(10)))
try:
	ast.parse(src)
	print('SYNTAX OK')
except SyntaxError as e:
	print('SYNTAX ERR:', e, 'line', e.lineno)
lines = src.split(chr(10))
key = chr(95) * 2 + 'name' + chr(95) * 2
for i, ln in enumerate(lines, 1):
	if key in ln:
		print('FOUND name at', i, repr(ln))
key2 = 'if name =='
for i, ln in enumerate(lines, 1):
	if key2 in ln:
		print('BAD name at', i, repr(ln))
print('done')
