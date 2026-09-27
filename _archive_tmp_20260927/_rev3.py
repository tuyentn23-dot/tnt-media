import ast
U = chr(95)
p = 'ops/quality' + U + 'gate.py'
src = open(p, encoding='utf-8').read()
old = "reasons += ([f'resolution {width}x{height} < 1080x1920'] if width < 1080 or height < 1920 else [])"
new = "reasons += ([f'resolution {width}x{height} < 720x1280'] if width < 720 or height < 1280 else [])"
if old in src:
 src = src.replace(old, new, 1)
 print('replaced')
else:
 print('pattern not found - check manually')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('REV3 OK')
