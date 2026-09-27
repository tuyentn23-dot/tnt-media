import ast
for p in ['ops/channel_style.py', 'ops/safe_io.py']:
 try:
 src = open(p, encoding='utf-8').read()
 ast.parse(src)
 print(p, 'OK')
 except SyntaxError as e:
 print(p, 'ERR line', e.lineno, ':', e.msg)
