import ast
NL = chr(10)
TB = chr(9)
TB2 = TB+TB
TB3 = TB+TB+TB

# ---- Patch tray.py ----
pt = 'app/tray.py'
src = open(pt, encoding='utf-8').read()

old_pause = (
 TB + 'def on_pause(icon=None, item=None):' + NL
 + TB2 + 'try:' + NL
 + TB3 + 'from pipeline import state as _st' + NL
 + TB3 + 'c = _st.init()' + NL
 + TB3 + 'c.execute("UPDATE channels SET enabled=0")' + NL
 + TB3 + 'c.commit()' + NL
 + TB3 + "print('[tray] da tam dung scheduler')" + NL
 + TB2 + 'except Exception as e:' + NL
 + TB3 + "print('[tray] pause ERR: ' + str(e)[:120])" + NL
)

new_pause = (
 TB + 'def on_pause(icon=None, item=None):' + NL
 + TB2 + 'try:' + NL
 + TB3 + 'import os as _os' + NL
 + TB3 + "_flag = _os.path.join(ROOT, 'state', 'paused.flag')" + NL
 + TB3 + '_os.makedirs(_os.path.dirname(_flag), exist_ok=True)' + NL
 + TB3 + "open(_flag, 'w').write('1')" + NL
 + TB3 + "print('[tray] da tam dung scheduler (flag)')" + NL
 + TB2 + 'except Exception as e:' + NL
 + TB3 + "print('[tray] pause ERR: ' + str(e)[:120])" + NL
)

old_resume = (
 TB + 'def on_resume(icon=None, item=None):' + NL
 + TB2 + 'try:' + NL
 + TB3 + 'from pipeline import state as _st' + NL
 + TB3 + 'c = _st.init()' + NL
 + TB3 + 'c.execute("UPDATE channels SET enabled=1")' + NL
 + TB3 + 'c.commit()' + NL
 + TB3 + "print('[tray] da tiep tuc scheduler')" + NL
 + TB2 + 'except Exception as e:' + NL
 + TB3 + "print('[tray] resume ERR: ' + str(e)[:120])" + NL
)

new_resume = (
 TB + 'def on_resume(icon=None, item=None):' + NL
 + TB2 + 'try:' + NL
 + TB3 + 'import os as _os' + NL
 + TB3 + "_flag = _os.path.join(ROOT, 'state', 'paused.flag')" + NL
 + TB3 + 'if _os.path.exists(_flag):' + NL
 + TB3 + TB + '_os.remove(_flag)' + NL
 + TB3 + "print('[tray] da tiep tuc scheduler (flag removed)')" + NL
 + TB2 + 'except Exception as e:' + NL
 + TB3 + "print('[tray] resume ERR: ' + str(e)[:120])" + NL
)

print('tray pause in src:', old_pause in src)
print('tray resume in src:', old_resume in src)
if old_pause in src and old_resume in src:
 src = src.replace(old_pause, new_pause, 1)
 src = src.replace(old_resume, new_resume, 1)
 open(pt, 'w', encoding='utf-8').write(src)
 print('tray PATCHED')

ast.parse(open(pt, encoding='utf-8').read())
print('tray AST OK')
