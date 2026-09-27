import ast
NL = chr(10)
TB = chr(9)
TB2 = TB+TB
p = 'pipeline/scheduler.py'
src = open(p, encoding='utf-8').read()

old = (
 'def tick():' + NL
 + TB + 'import time as tmod' + NL
 + TB + 'now = tmod.localtime()' + NL
 + TB + 'c = state.connect()' + NL
 + TB + "rows = c.execute('SELECT id, schedule FROM channels WHERE enabled=1').fetchall()" + NL
)

new = (
 'def tick():' + NL
 + TB + 'import time as tmod' + NL
 + TB + "import os as _os" + NL
 + TB + "_flag = _os.path.join(ROOT, 'state', 'paused.flag')" + NL
 + TB + 'if _os.path.exists(_flag):' + NL
 + TB2 + "print('[scheduler] paused - skip tick')" + NL
 + TB2 + 'return 0' + NL
 + TB + 'now = tmod.localtime()' + NL
 + TB + 'c = state.connect()' + NL
 + TB + "rows = c.execute('SELECT id, schedule FROM channels WHERE enabled=1').fetchall()" + NL
)

print('old in src:', old in src)
if old in src:
 src = src.replace(old, new, 1)
 open(p, 'w', encoding='utf-8').write(src)
 print('PATCHED')
else:
 print('NOT FOUND')

ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
