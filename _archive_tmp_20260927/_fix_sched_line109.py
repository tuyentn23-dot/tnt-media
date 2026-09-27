import ast
NL = chr(10)
TB = chr(9)
TB2 = TB+TB
Q = chr(39)
p = 'pipeline/scheduler.py'
lines = open(p, encoding='utf-8').read().splitlines(keepends=True)

bad_idx = 108
print('BEFORE:', repr(lines[bad_idx]))

sql = 'SELECT id FROM jobs WHERE status=? AND run_at IS NOT NULL AND run_at <= ?'
fixed = TB2 + 'rows_at = c.execute(' + Q + sql + Q + ', (' + Q + 'scheduled' + Q + ', state.now())).fetchall()' + NL
lines[bad_idx] = fixed

open(p, 'w', encoding='utf-8', newline='').write(''.join(lines))
print('AFTER :', repr(fixed))

try:
 ast.parse(open(p, encoding='utf-8').read())
 print('AST OK')
except SyntaxError as e:
 print('AST ERR line', e.lineno, ':', e.msg)
