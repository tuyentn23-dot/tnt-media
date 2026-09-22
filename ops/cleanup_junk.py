# -*- coding: utf-8 -*-
# ops/cleanup_junk.py - Don file video rac/loi trong output
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, 'output')
MIN_SIZE = 300000

def clean(min_size=MIN_SIZE, dry=False):
    removed = []
    if not os.path.isdir(OUTPUT):
        return removed
    for f in os.listdir(OUTPUT):
        if not f.lower().endswith('.mp4'):
            continue
        p = os.path.join(OUTPUT, f)
        try:
            sz = os.path.getsize(p)
        except Exception:
            continue
        if sz < min_size:
            if not dry:
                try:
                    os.remove(p)
                except Exception:
                    continue
            removed.append((f, sz))
    return removed

if __name__ == '__main__':
    r = clean()
    print('removed', len(r), 'junk files')
    for f, sz in r:
        print(' -', f, sz)
