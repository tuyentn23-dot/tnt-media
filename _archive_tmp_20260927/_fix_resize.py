import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
L = open(p, encoding='utf-8').read().split(NL)
new_L = []
for i, l in enumerate(L):
	if 'resized(height=1280)' in l or 'resize(height=1280)' in l:
		new_L.append(T + T + '_pil = Image.fromarray(_c.get_frame(0)).resize((720, 1280))')
		new_L.append(T + T + 'b = V(np.array(_pil))')
		print('fixed line', i + 1)
	else:
		new_L.append(l)
content = NL.join(new_L)
open(p, 'w', encoding='utf-8').write(content)
try:
	ast.parse(content); print('RESIZE OK, lines:', len(new_L))
except Exception as e:
	print('ERR:', e)
