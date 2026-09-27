import ast
NL = chr(10)
SP = chr(32)
SP4 = SP+SP+SP+SP
SP8 = SP4+SP4
p = 'ops/os_publish.py'
src = open(p, encoding='utf-8').read()

old = SP4 + 'except Exception as _he:' + NL + SP8 + 'pass' + NL + NL + SP4 + 'from ops import quality_rules as _qr'
ret = SP8 + "return {'ok': False, 'blocked': True, 'reason': 'video-health-exception', 'error': str(_he)}"
new = SP4 + 'except Exception as _he:' + NL + ret + NL + NL + SP4 + 'from ops import quality_rules as _qr'

print('old in src:', old in src)
if old in src:
 src = src.replace(old, new, 1)
 open(p, 'w', encoding='utf-8').write(src)
 print('PATCHED')
else:
 print('NOT FOUND')

ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
