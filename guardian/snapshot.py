# -- coding: utf-8 --
# guardian/snapshot.py - Snapshot + restore file quan trong.
import os, json, shutil, hashlib, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP_DIR = os.path.join(ROOT, 'guardian', 'snapshots')
CRIT = os.path.join(ROOT, 'guardian', 'critical.json')

def _critical():
    d = json.load(open(CRIT, encoding='utf-8'))
    out = []
    for k, v in d.items():
        out += v
    return out

def _hash(path):
    h = hashlib.sha256()
    h.update(open(path, 'rb').read())
    return h.hexdigest()[:16]

def snapshot(tag=''):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M-S')
    d = os.path.join(SNAP_DIR, ts + (('_' + tag) if tag else ''))
    os.makedirs(d, exist_ok=True)
    manifest = {}
    for rel in _critical():
        src = os.path.join(ROOT, rel)
        if os.path.exists(src):
            dst = os.path.join(d, rel.replace('/', '__'))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            manifest[rel] = _hash(src)
    json.dump(manifest, open(os.path.join(d, '_manifest.json'), 'w'), indent=1)
    print('SNAPSHOT OK:', d, '(', len(manifest), 'files)')
    return d

def verify():
    d = _critical()
    missing = [f for f in d if not os.path.exists(os.path.join(ROOT, f))]
    print('MISSING:', missing if missing else 'none')
    return missing

def restore(snap_dir=None):
    if not snap_dir:
        snaps = sorted(os.listdir(SNAP_DIR)) if os.path.isdir(SNAP_DIR) else []
        if not snaps:
            print('no snapshots')
            return
        snap_dir = os.path.join(SNAP_DIR, snaps[-1])
    mf = json.load(open(os.path.join(snap_dir, '_manifest.json')))
    n = 0
    for rel in mf:
        src = os.path.join(snap_dir, rel.replace('/', '__'))
        dst = os.path.join(ROOT, rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            n += 1
    print('RESTORED', n, 'files from', os.path.basename(snap_dir))

if __name__ == '__main__':
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'snapshot'
    if cmd == 'snapshot':
        snapshot()
    elif cmd == 'verify':
        verify()
    elif cmd == 'restore':
        restore()
