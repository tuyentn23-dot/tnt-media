import subprocess
v='assets/song_lang_im_thuong_anh.mp4'
r=subprocess.run(['tools/ffmpeg.exe','-i',v], capture_output=True, text=True, encoding='utf-8', errors='replace')
for l in (r.stderr or '').splitlines():
    if 'Duration' in l or 'Stream' in l:
        print(l.strip().encode('ascii','replace').decode('ascii'))
print('--- vinyl loop ---')
import os
for f in os.listdir('E:/OneDrive/Desktop'):
    if 'vinyl' in f.lower():
        print(f, os.path.getsize(os.path.join('E:/OneDrive/Desktop',f)))
