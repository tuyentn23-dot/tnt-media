import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
old = T + T + 'base.alpha' + U + 'composite(overlay)'
new = T + T + 'base = Image.alpha' + U + 'composite(base, overlay)'
if old in src:
	src = src.replace(old, new, 1)
	print('FIXED')
else:
	print('NOT FOUND')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('PIL4 OK')
