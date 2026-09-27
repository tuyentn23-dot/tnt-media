import ast
p = 'ops/channel_style.py'
src = open(p, 'rb').read()
TB = bytes([9])
LF = bytes([10])

# Lines 46-49 need extra tab (they belong inside for loop)
old = (
 TB + b'for ln in lines:' + LF
 + TB + b'w = dr.textlength(ln, font=font)' + LF
 + TB + b'x = (W - w) / 2' + LF
 + TB + b"dr.text((x, cy), ln, font=font, fill=color, stroke_width=4, stroke_fill='black')" + LF
 + TB + b'cy += lh' + LF
)

new = (
 TB + b'for ln in lines:' + LF
 + TB + TB + b'w = dr.textlength(ln, font=font)' + LF
 + TB + TB + b'x = (W - w) / 2' + LF
 + TB + TB + b"dr.text((x, cy), ln, font=font, fill=color, stroke_width=4, stroke_fill='black')" + LF
 + TB + TB + b'cy += lh' + LF
)

print('old in src:', old in src)
if old in src:
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
