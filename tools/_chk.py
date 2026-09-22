import ast
t=open('ops/mia_content.py',encoding='utf-8').read()
ast.parse(t)
print('syntax OK lines', t.count(chr(10))+1)
