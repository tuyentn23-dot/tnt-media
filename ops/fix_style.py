import ast, sys
p = 'ops/channel_style.py'
src = open(p, encoding='utf-8').read()
try:
	ast.parse(src)
	print('already OK')
	sys.exit(0)
except SyntaxError as e:
	print('ERR line', e.lineno)
	lines = src.split(chr(10))
	print('context:')
	for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+8)):
		print(i+1, repr(lines[i]))
