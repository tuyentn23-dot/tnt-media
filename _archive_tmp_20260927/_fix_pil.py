import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
old = T + 'overlay = text' + U + 'frame(text, fs, col, 720, 1280, y)'
new = T + 'overlay = Image.fromarray(text' + U + 'frame(text, fs, col, 720, 1280, y)).convert(' + DQ + 'RGBA' + DQ + ')'
if old in src:
	src = src.replace(old, new, 1)
	print('FIXED line overlay')
else:
	print('overlay pattern NOT FOUND')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('FIX PIL OK')
