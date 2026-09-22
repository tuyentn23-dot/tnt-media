# -*- coding: utf-8 -*-
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
SONG = os.path.join(ROOT, 'assets', 'song_lang_im_thuong_anh.mp4')
LOOP = os.path.join(ROOT, 'assets', 'youtube_love_vinyl_dynamic_loop.mp4')
OUT = os.path.join(ROOT, 'output', 'vile_lang_im_thuong_anh.mp4')
THUMB = os.path.join(ROOT, 'output', 'vile_lang_im_thuong_anh_thumb.jpg')
os.makedirs(os.path.join(ROOT, 'output'), exist_ok=True)

# 1) Video: loop vinyl + audio bai hat
def dur(p):
    r=subprocess.run([FF,'-i',p], capture_output=True, text=True, encoding='utf-8', errors='replace')
    for l in (r.stderr or '').splitlines():
        if 'Duration' in l:
            t=l.split('Duration:')[1].split(',')[0].strip()
            h,m,s=t.split(':')
            return int(h)*3600+int(m)*60+float(s)
    return 0
d = dur(SONG)
print('song duration', d)
cmd=[FF,'-y','-stream_loop','-1','-i',LOOP,'-i',SONG,'-map','0:v','-map','1:a','-t',str(d),'-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-vf','scale=1920:1080','-c:a','aac','-b:a','192k','-shortest',OUT]
r=subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('video rc', r.returncode)
if os.path.exists(OUT):
    print('OUT', os.path.getsize(OUT))
