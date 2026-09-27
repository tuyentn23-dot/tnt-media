import ast
U = chr(95) + chr(95)
Q = chr(39)
p = 'pipeline/scheduler.py'
src = open(p, encoding='utf-8').read()

src = src.replace('os.path.abspath(file)', 'os.path.abspath(' + U + 'file' + U + ')')

old = 'if name == ' + Q + 'main' + Q + ':'
new = 'if ' + U + 'name' + U + ' == ' + Q + U + 'main' + U + Q + ':'
src = src.replace(old, new)

open(p, 'w', encoding='utf-8', newline='').write(src)
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
print('FILE DUNDER present:', (U + 'file' + U) in open(p, encoding='utf-8').read())
