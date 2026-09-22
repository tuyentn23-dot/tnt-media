import subprocess, os
import numpy as np
from PIL import Image
v='output/_test_vile_191715.mp4'
for t in ['1','5','10']:
    png=v+'.'+t+'.png'
    subprocess.run(['tools/ffmpeg.exe','-y','-ss',t,'-i',v,'-frames:v','1',png], capture_output=True)
    a=np.asarray(Image.open(png).convert('RGB'), dtype='float32')
    print(t, round(float(a.mean()),1), round(float(a.std()),1))
