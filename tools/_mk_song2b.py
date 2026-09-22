# -*- coding: utf-8 -*-
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
COVER = os.path.join(ROOT, 'assets', 'youaremyonlyone_cover.png')
SONG = os.path.join(ROOT, 'assets', 'song_youaremyonlyone.m4a')
OUT = os.path.join(ROOT, 'output', 'vile_youaremyonlyone.mp4')
D = 209.58
fc = (
 "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=30[bg];"
 "[0:v]scale=-1:1000[fg];"
 "[bg][fg]overlay=(W-w)/2:(H-h)/2[ov];"
 "[ov]zoompan=z='min(zoom+0.0003,1.12)':d="+str(int(D*30))+":s=1920x1080:fps=30[v]"
)
cmd=[FF,'-y','-loop','1','-i',COVER,'-i',SONG,'-filter_complex',fc,'-map','[v]','-map','1:a','-t',str(D),'-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',OUT]
print('running...')
r=subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('rc', r.returncode)
print('OUT', os.path.getsize(OUT) if os.path.exists(OUT) else 0)
if r.returncode!=0:
    print(r.stderr[-400:].encode('ascii','replace').decode('ascii'))
