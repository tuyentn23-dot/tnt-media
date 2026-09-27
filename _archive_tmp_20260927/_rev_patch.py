import ast
U = chr(95)
p = 'ops/channel' + U + 'style.py'
src = open(p, encoding='utf-8').read()
src = src.replace('W, H = 1080, 1920', 'W, H = 720, 1280')
src = src.replace('W, H = 1920, 1080', 'W, H = 1280, 720')
src = src.replace('W=1080, H=1920, y=450', 'W=720, H=1280, y=300')
src = src.replace("fs = int(style.get('font_size', 66))", "fs = int(style.get('font_size', 44))")
src = src.replace('y=H - 210', 'y=H - 140')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('PATCH OK')
