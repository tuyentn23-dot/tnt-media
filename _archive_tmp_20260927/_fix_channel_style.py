import ast
p = 'ops/channel_style.py'
src = open(p, 'rb').read()

TB = bytes([9])
LF = bytes([10])

old = (
 TB + b'try:' + LF
 + TB + b'font = ImageFont.truetype(font_path, fs)' + LF
 + TB + b'except Exception:' + LF
 + TB + b'font = ImageFont.truetype(FONT, fs)' + LF
)

new = (
 TB + b'try:' + LF
 + TB + TB + b'font = ImageFont.truetype(font_path, fs)' + LF
 + TB + b'except Exception:' + LF
 + TB + TB + b'font = ImageFont.truetype(FONT, fs)' + LF
)

print('old in src:', old in src)
n = src.count(old)
print('occurrences:', n)
if n > 0:
 src = src.replace(old, new, 1)
 open(p, 'wb').write(src)
 print('PATCHED')
else:
 print('NOT FOUND')

try:
 ast.parse(open(p, encoding='utf-8').read())
 print('AST OK')
except SyntaxError as e:
 print('AST ERR line', e.lineno, ':', e.msg)
