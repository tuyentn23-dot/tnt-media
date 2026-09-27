import ast
U = chr(95) + chr(95)
Q = chr(39)
p = 'pipeline/scheduler.py'
src = open(p, encoding='utf-8').read()

src = src.replace('FILEMARK', U + 'file' + U)
src = src.replace('MAINMARK', U + 'name' + U)
src = src.replace('MAINVAL', U + 'main' + U)

open(p, 'w', encoding='utf-8', newline='').write(src)
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
print('has file:', (U + 'file' + U) in open(p, encoding='utf-8').read())
print('has name:', (U + 'name' + U) in open(p, encoding='utf-8').read())
print('has main:', (U + 'main' + U) in open(p, encoding='utf-8').read())
