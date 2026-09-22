import ast, sys
fn = sys.argv[1] if len(sys.argv) > 1 else 'ops/build_pika_mv2.py'
src = open(fn, encoding='utf-8').read()
print('file:', fn)
print('len:', len(src), 'lines:', src.count(chr(10)))
try:
	ast.parse(src)
	print('SYNTAX OK')
except SyntaxError as e:
	print('ERR:', e, 'line', e.lineno)
	lines = src.split(chr(10))
	if e.lineno:
		for i in range(max(0, e.lineno - 3), min(len(lines), e.lineno + 2)):
			print(i + 1, repr(lines[i]))
