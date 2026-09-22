import os, subprocess
import numpy as np
from PIL import Image
def m(v):
    png=v+'.c.png'
    subprocess.run(['tools/ffmpeg.exe','-y','-ss','1','-i',v,'-frames:v','1',png], capture_output=True)
    if not os.path.exists(png): return None
    a=np.asarray(Image.open(png).convert('RGB'), dtype='float32')
    r=(round(float(a.mean()),1), round(float(a.std()),1))
    os.remove(png)
    return r
for kind in ['lifestyle','food','animals','nostalgia','curiosity']:
    d='library/'+kind
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if f.lower().endswith('.mp4'):
            print(kind, f, os.path.getsize(os.path.join(d,f)), m(os.path.join(d,f)))
