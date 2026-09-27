import ast
U = chr(95); NL = chr(10)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
src = src.replace('cmp_editor()[5]', U + 'cmp' + U + 'editor()[5]')
open(p, 'w', encoding='utf-8').write(src)
try:
	ast.parse(src)
	print('FIX CMP OK')
except Exception as e:
	print('ERR:', e)
	L = src.split(NL)
	for i in range(48, 85):
		print(i + 1, repr(L[i])[:140])
