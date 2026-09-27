import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
L = open(p, encoding='utf-8').read().split(NL)
for i, l in enumerate(L):
	if 'convert(' + DQ + 'RGB' + DQ + ').' in l and 'array' in l:
		L[i] = T + T + 'import numpy as np' + NL + T + T + 'return np.array(base.convert(' + DQ + 'RGB' + DQ + '))'
		print('fixed line', i + 1)
content = NL.join(L)
open(p, 'w', encoding='utf-8').write(content)
ast.parse(content)
print('PIL3 OK')
