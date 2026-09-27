import os, sys
ROOT = os.getcwd()
sys.path.insert(0, ROOT)
S = chr(32)
S4 = S+S+S+S
S8 = S4+S4
L = []
L.append('import os, sys')
L.append('ROOT = os.getcwd()')
L.append('sys.path.insert(0, ROOT)')
L.append('from pipeline import state')
L.append('c = state.init()')
L.append('checks = [(\'publications\', "status=\'pending_approval\'"), (\'publications\', "status=\'approved\'"), (\'jobs\', \'1=1\')]')
L.append('for table, where in checks:')
L.append(S4 + 'try:')
L.append(S8 + 'n = c.execute(\'SELECT COUNT(*) FROM \' + table + \' WHERE \' + where).fetchone()[0]')
L.append(S8 + 'print(table, where, \'->\', n)')
L.append(S4 + 'except Exception as e:')
L.append(S8 + 'print(\'ERR\', table, e)')
L.append('rows = c.execute("SELECT id, channel_id, topic, title, created_at FROM publications WHERE status=\'pending_approval\' ORDER BY created_at DESC LIMIT 5").fetchall()')
L.append('for r in rows:')
L.append(S4 + 'print(dict(r))')
open('ops/_count_pending.py','w',encoding='utf-8').write(chr(10).join(L) + chr(10))
import ast
ast.parse(open('ops/_count_pending.py',encoding='utf-8').read())
print('AST OK')