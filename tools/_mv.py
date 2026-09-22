src = open('tools/_mia_src.txt', encoding='utf-8').read()
open('ops/mia_content.py', 'w', encoding='utf-8').write(src)
import ast
ast.parse(src)
print('moved and syntax OK, lines', src.count(chr(10))+1)
