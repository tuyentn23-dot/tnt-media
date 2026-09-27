U = chr(95) + chr(95)
p = 'ops/_test_cron.py'
src = open(p, encoding='utf-8').read()
src = src.replace('FILEMARK', U + 'file' + U)
open(p, 'w', encoding='utf-8', newline='').write(src)
import ast
ast.parse(src)
print('AST OK')
print('has dunder file:', (U + 'file' + U) in src)
