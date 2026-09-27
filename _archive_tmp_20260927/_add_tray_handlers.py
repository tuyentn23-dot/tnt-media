import ast
NL = chr(10)
TB = chr(9)
TB2 = TB+TB
Q = chr(39)
p = 'app/tray.py'
src = open(p, encoding='utf-8', newline='').read()

target = TB + 'def on_quit(icon, item):'
assert target in src

L = []
L.append(TB + 'def on_open_logs(icon=None, item=None):')
L.append(TB2 + 'try:')
L.append(TB2 + TB + 'logdir = os.path.join(ROOT, ' + Q + 'logs' + Q + ')')
L.append(TB2 + TB + 'os.makedirs(logdir, exist_ok=True)')
L.append(TB2 + TB + 'os.startfile(logdir)')
L.append(TB2 + 'except Exception as e:')
L.append(TB2 + TB + 'print(' + Q + '[tray] open logs ERR: ' + Q + ' + str(e)[:120])')
L.append(TB + 'def on_backup_now(icon=None, item=None):')
L.append(TB2 + 'try:')
L.append(TB2 + TB + 'from ops import backup_state as _bs')
L.append(TB2 + TB + 'from pipeline import state as _st')
L.append(TB2 + TB + 'bk = os.path.join(ROOT, ' + Q + 'state' + Q + ', ' + Q + 'backup' + Q + ')')
L.append(TB2 + TB + 'dst = _bs.backup_sqlite(_st.DB, bk)')
L.append(TB2 + TB + 'print(' + Q + '[tray] backup: ' + Q + ' + dst)')
L.append(TB2 + 'except Exception as e:')
L.append(TB2 + TB + 'print(' + Q + '[tray] backup ERR: ' + Q + ' + str(e)[:120])')
new_handlers = NL.join(L) + NL

old_menu6 = TB + 'm6 = pystray.MenuItem(' + Q + 'Xem loi (log)' + Q + ', on_open)'
new_menu6 = TB + 'm6 = pystray.MenuItem(' + Q + 'Xem log' + Q + ', on_open_logs)' + NL + TB + 'm6b = pystray.MenuItem(' + Q + 'Backup ngay' + Q + ', on_backup_now)'
assert old_menu6 in src, 'menu6 not found'
src = src.replace(old_menu6, new_menu6, 1)

old_menu = TB + 'menu = pystray.Menu(m1, m2, pystray.Menu.SEPARATOR, m3, m4, pystray.Menu.SEPARATOR, m5, m6, pystray.Menu.SEPARATOR, m7)'
new_menu = TB + 'menu = pystray.Menu(m1, m2, pystray.Menu.SEPARATOR, m3, m4, pystray.Menu.SEPARATOR, m5, m6, m6b, pystray.Menu.SEPARATOR, m7)'
assert old_menu in src, 'menu not found'
src = src.replace(old_menu, new_menu, 1)

src = src.replace(target, new_handlers + target, 1)

open(p, 'w', encoding='utf-8', newline='').write(src)
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
