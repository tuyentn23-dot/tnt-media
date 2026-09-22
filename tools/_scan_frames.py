import os, subprocess
import numpy as np
from PIL import Image

def frames(v):
    # lay 5 frame: 1s, 25%, 50%, 75%, cuoi
    dur = None
    r = subprocess.run(['tools/ffmpeg.exe','-i',v], capture_output=True, text=True, encoding='utf-8', errors='replace')
    for line in (r.stderr or '').splitlines():
        if 'Duration' in line:
            t = line.split('Duration:')[1].split(',')[0].strip()
            h,m,s = t.split(':')
            dur = int(h)*3600+int(m)*60+float(s)
    if not dur:
        return []
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

files = [f for f in os.listdir('output') if f.startswith('chMialinhcute') or f.startswith('chvilevi5676')]
for f in sorted(files):
    p = os.path.join('output', f)
    if os.path.getsize(p) < 500000:
        continue
    fr = frames(p)
    means = [x[0] for x in fr]
    black = sum(1 for m,s in fr if m < 12 and s < 25)
    tag = 'HAS-BLACK' if black else 'OK'
    print(tag, f, 'means=', means)
