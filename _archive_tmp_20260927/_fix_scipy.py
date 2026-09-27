import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
src = src.replace('resized(height=1280, pillow=False)', 'resized(height=1280, method=' + Q + 'scipy' + Q + ')')
src = src.replace('resize(height=1280, pillow=False)', 'resize(height=1280, method=' + Q + 'scipy' + Q + ')')
src = src.replace('resized(width=720, pillow=False)', 'resized(width=720, method=' + Q + 'scipy' + Q + ')')
src = src.replace('resize(width=720, pillow=False)', 'resize(width=720, method=' + Q + 'scipy' + Q + ')')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('SCIPY PATCH OK')
