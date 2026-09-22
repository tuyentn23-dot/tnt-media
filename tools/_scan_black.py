import os, subprocess
import numpy as np
from PIL import Image

def frame_mean(v, t='2'):
    out = v + '.chk.png'
    r = subprocess.run(['tools/ffmpeg.exe','-y','-ss',t,'-i',v,'-frames:v','1',out], capture_output=True)
    if not os.path.exists(out):
        return None
    a = np.asarray(Image.open(out).convert('RGB'), dtype='float32')
    m = float(a.mean()); s = float(a.std())
    try: os.remove(out)
    except Exception: pass
    return m, s

roots = ['output']
rows = []
for r in roots:
    for f in os.listdir(r):
        if not f.endswith('.mp4'):
            continue
        if not (f.startswith('chMialinhcute') or f.startswith('chvilevi5676')):
            continue
        p = os.path.join(r, f)
        sz = os.path.getsize(p)
        if sz < 200000:
            rows.append((f, sz, 'TOO_SMALL', 0, 0))
            continue
        fr = frame_mean(p)
        if fr is None:
            rows.append((f, sz, 'BAD_FILE', 0, 0))
        else:
            m, s = fr
            status = 'BLACK' if (m < 12 and s < 25) else 'OK'
            rows.append((f, sz, status, round(m,1), round(s,1)))

for f, sz, st, m, s in sorted(rows):
    print(st, f, sz, 'mean='+str(m), 'std='+str(s))
print('TOTAL', len(rows), 'BLACK', len([x for x in rows if x[2]=='BLACK']), 'SMALL', len([x for x in rows if x[2]=='TOO_SMALL']))
