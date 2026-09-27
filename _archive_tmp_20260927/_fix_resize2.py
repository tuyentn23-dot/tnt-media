import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
src = src.replace('resized(height=1280)', 'resized(height=1280, pillow=False)')
src = src.replace('resize(height=1280)', 'resize(height=1280, pillow=False)')
src = src.replace('resized(width=720)', 'resized(width=720, pillow=False)')
src = src.replace('resize(width=720)', 'resize(width=720, pillow=False)')
src = src.replace('b.resized(height=1280)', 'b.resized(height=1280, pillow=False)')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('FIX_RESIZE2 OK')
