# Patch: remove force=True in _routes_publish.py
import ast
p = 'app/_routes_publish.py'
src = open(p, encoding='utf-8').read()
old = chr(44) + ' force=True)'
new = chr(41)
if old in src:
 src = src.replace(old, new)
 open(p, 'w', encoding='utf-8').write(src)
 print('PATCHED: removed force=True')
else:
 print('NOT FOUND')
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
