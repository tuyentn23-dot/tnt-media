import os, subprocess
import numpy as np
from PIL import Image
def frames(v):
    r = subprocess.run(['tools/ffmpeg.exe','-i',v], capture_output=True, text=True, encoding='utf-8', errors='replace')
    dur = None
    for line in (r.stderr or '').splitlines():
        if 'Duration' in line:
            t = line.split('Duration:')[1].split(',')[0].strip()
            h,m,s = t.split(':')
            dur = int(h)*3600+int(m)*60+float(s)
    if not dur: return []
    ts = [1, dur*0.25, dur*0.5, dur*0.75, max(1, dur-1)]
    out = []
    for t in ts:
        png = v + '.f.png'
        subprocess.run(['tools/ffmpeg.exe','-y','-ss',str(t),'-i',v,'-frames:v','1',png], capture_output=True)
        if os.path.exists(png):
            a = np.asarray(Image.open(png).convert('RGB'), dtype='float32')
            out.append((round(float(a.mean()),1), round(float(a.std()),1)))
            os.remove(png)
    return out
for f in sorted(os.listdir('output')):
    if not f.startswith('chvilevi5676'):
        continue
    p = os.path.join('output', f)
    fr = frames(p)
    black = sum(1 for m,s in fr if m < 12 and s < 25)
    print(('BLACK' if black else 'OK'), f, os.path.getsize(p), [x[0] for x in fr])
