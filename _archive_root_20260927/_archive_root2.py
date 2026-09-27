import os, shutil
UND = chr(95)
TARGET = UND + 'archive_root_20260927'
os.makedirs(TARGET, exist_ok=True)
moved = []
for f in os.listdir('.'):
    if not os.path.isfile(f): continue
    if not f.startswith(UND): continue
    if f == '_serve.py': continue
    if f == '_archive_root.py': continue
    ext = f.rsplit('.', 1)[-1].lower() if '.' in f else ''
    if ext not in ('py', 'txt', 'json', 'html'): continue
    try:
         shutil.move(f, os.path.join(TARGET, f))
         moved.append(f)
    except Exception as e:
         print('skip', f, e)
print('moved:', len(moved))
for f in sorted(moved): print(' ', f)
