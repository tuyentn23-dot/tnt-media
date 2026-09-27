NL = chr(10)
p = 'pipeline/scheduler.py'
lines = open(p, encoding='utf-8').read().splitlines(keepends=True)
bad_idx = 48 # line 49
print('BEFORE:', repr(lines[bad_idx]))
lines[bad_idx] = "			'weekday': _expand_cron_field(p[4], 0, 6)," + NL
open(p, 'w', encoding='utf-8', newline='').write(''.join(lines))
print('AFTER :', repr(lines[bad_idx]))
import ast
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
