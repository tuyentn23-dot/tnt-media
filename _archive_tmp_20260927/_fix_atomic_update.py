import ast
NL = chr(10)
TB = chr(9)
p = 'app/_routes_publish.py'
src = open(p, encoding='utf-8').read()

old = (
 TB + "c.execute('UPDATE publications SET status=? WHERE id=?', ('publishing', pub_id))" + NL
 + TB + 'c.commit()' + NL
)

new = (
 TB + "cur2 = c.execute('UPDATE publications SET status=? WHERE id=? AND status=?', ('publishing', pub_id, cur))" + NL
 + TB + 'c.commit()' + NL
 + TB + 'if cur2.rowcount != 1:' + NL
 + TB + TB + "return JSONResponse({'ok': False, 'error': 'publication da duoc xu ly boi request khac', 'status': 'publishing'}, status_code=409)" + NL
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
