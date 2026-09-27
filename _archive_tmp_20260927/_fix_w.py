import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
src = src.replace('width=1080)', 'width=720)')
src = src.replace('height=1920)', 'height=1280)')
src = src.replace('width=1080, height=1280', 'width=720, height=1280')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('FIX_W OK')
