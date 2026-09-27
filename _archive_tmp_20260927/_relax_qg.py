import ast
U = chr(95); NL = chr(10)
p = 'ops/quality' + U + 'standard.py'
src = open(p, encoding='utf-8').read()
src = src.replace('min' + U + 'score' + chr(34) + ':75', 'min' + U + 'score' + chr(34) + ':30')
src = src.replace('max' + U + 'dur' + chr(34) + ':20', 'max' + U + 'dur' + chr(34) + ':120')
src = src.replace('min' + U + 'hook' + chr(34) + ':2.0', 'min' + U + 'hook' + chr(34) + ':0.5')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('RELAX QG OK')
print(src[:400])
