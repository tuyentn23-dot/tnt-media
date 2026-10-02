# -- coding: utf-8 --
# guardian/guard.py - Bao ve he thong.
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def before_task(tag=''):
    from guardian import snapshot as sn
    return sn.snapshot(tag)

def after_task():
    from guardian import snapshot as sn
    m = sn.verify()
    if m:
        print('GUARD WARN: missing ', m)
    return m

def safe_rm(paths):
    from guardian import safe_fs as sf
    return sf.safe_remove(paths)

def safe_mv(src, dst):
    from guardian import safe_fs as sf
    return sf.safe_move(src, dst)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'verify'
    if cmd == 'before':
        before_task()
    elif cmd == 'verify':
        after_task()
