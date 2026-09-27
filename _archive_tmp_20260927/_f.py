import ast
U = chr(95); NL = chr(10)
p = 'ops/content' + U + 'video5.py'
src = open(p, encoding='utf-8').read()
src = src.replace('cmp_editor()[5]', '' + U + 'cmp_editor()[5]')
src = src.replace('# append make_scene_v2 - khong dung moviepy resize', '')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('FIX OK')
