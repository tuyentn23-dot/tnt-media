# -- coding: utf-8 --
# guardian/safe_fs.py - Thao tac file AN TOAN. Khong xoa ngoai _trash.
import os, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(ROOT, '_trash', 'archive')

def _arch():
    d = os.path.join(ARCHIVE, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    os.makedirs(d, exist_ok=True)
    return d

def safe_remove(paths):
    if isinstance(paths, str):
        paths = [paths]
    d = _arch()
    n = 0
    for p in paths:
        if not os.path.exists(p):
            continue
        dst = os.path.join(d, os.path.basename(p))
        shutil.move(p, dst)
        n += 1
    print('ARCHIVED ', n, ' files to ', d)
    return d

def safe_move(src, dst):
    if not os.path.exists(src):
        print('SOURCE NOT FOUND ', src); return False
    d = os.path.dirname(dst) or '.'
    os.makedirs(d, exist_ok=True)
    shutil.move(src, dst)
    print('MOVED ', src, ' -> ', dst)
    return True

def list_arch():
    if not os.path.isdir(ARCHIVE):
        print('no archive'); return
    for d in sorted(os.listdir(ARCHIVE), reverse=True):
        fs = os.listdir(os.path.join(ARCHIVE, d))
        print(d, '(', len(fs), ' files)')

def restore_arch(ts):
    src = os.path.join(ARCHIVE, ts)
    if not os.path.isdir(src):
        print('not found ', ts); return
    n = 0
    for f in os.listdir(src):
        dst = os.path.join(ROOT, f)
        if not os.path.exists(dst):
            shutil.move(os.path.join(src, f), dst)
            n += 1
    print('RESTORED ', n, ' files')

if __name__ == '__main__':
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'list':
        list_arch()
    elif cmd == 'remove':
        safe_remove(sys.argv[2:])
    elif cmd == 'restore':
        restore_arch(sys.argv[2])
