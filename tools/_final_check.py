import os, subprocess
import numpy as np
from PIL import Image
def m(v):
    png=v+'.c.png'
    subprocess.run(['tools/ffmpeg.exe','-y','-ss','2','-i',v,'-frames:v','1',png], capture_output=True)
    if not os.path.exists(png): return None
    a=np.asarray(Image.open(png).convert('RGB'), dtype='float32')
    r=(round(float(a.mean()),1), round(float(a.std()),1))
    os.remove(png)
    return r
print('=== MIA ===')
for f in sorted(os.listdir('output')):
    if f.startswith('chMialinhcute') and os.path.getsize('output/'+f) > 400000:
        print(' ', f, m(os.path.join('output',f)))
print('=== VILE ===')
for f in sorted(os.listdir('output')):
    if f.startswith('chvilevi5676') and os.path.getsize('output/'+f) > 400000:
        print(' ', f, m(os.path.join('output',f)))
