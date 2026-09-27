import ast
NL = chr(10)
TB = chr(9)
TB3 = TB+TB+TB
TB4 = TB3+TB
TB5 = TB4+TB
p = 'pipeline/runner.py'
src = open(p, encoding='utf-8', newline='').read()

old = (
 TB4 + "r = _call('render.video', 'render', item, out, style=style)" + NL
 + TB4 + 'if r is None:' + NL
 + TB5 + 'from ops import channel_style as cs' + NL
 + TB5 + 'cs.build_styled(item, out, style=style)' + NL
)

new = (
 TB4 + "r = _call('render.video', 'render', item, out, style=style)" + NL
)

print('old in src:', old in src)
if old in src:
 src = src.replace(old, new, 1)
 open(p, 'w', encoding='utf-8', newline='').write(src)
 print('PATCHED')
else:
 print('NOT FOUND')

ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
