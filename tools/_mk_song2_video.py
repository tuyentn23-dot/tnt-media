# -*- coding: utf-8 -*-
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
COVER = os.path.join(ROOT, 'assets', 'youaremyonlyone_cover.png')
SONG = os.path.join(ROOT, 'assets', 'song_youaremyonlyone.webm')
OUT = os.path.join(ROOT, 'output', 'vile_youaremyonlyone.mp4')

def dur(p):
    r=subprocess.run([FF,'-i',p], capture_output=True, text=True, encoding='utf-8', errors='replace')
    for l in (r.stderr or '').splitlines():
        if 'Duration' in l:
            t=l.split('Duration:')[1].split(',')[0].strip()
            parts=t.split(':')
            if len(parts)==3:
                h,m,s=parts
                return int(h)*3600+int(m)*60+float(s)
            elif len(parts)==2:
                m,s=parts
                return int(m)*60+float(s)
    return 0
d = dur(SONG)
print('song dur', d)
# Anh bia 1214x1295 -> nen 1920x1080 blur + anh bia o giua co hieu ung zoom nhe
# filter: tao nen blur fill 1920x1080, overlay anh bia (fit height 1080) voi zoompan
fc = (
 "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=30[bg];"
 "[0:v]scale=-1:1080[fg];"
 "[bg][fg]overlay=(W-w)/2:(H-h)/2[ov];"
 "[ov]zoompan=z='min(zoom+0.0005,1.15)':d="+str(int(d*30))+":s=1920x1080:fps=30[v]"
)
cmd=[FF,'-y','-loop','1','-i',COVER,'-i',SONG,'-filter_complex',fc,'-map','[v]','-map','1:a','-t',str(d),'-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',OUT]
r=subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('rc', r.returncode)
if os.path.exists(OUT):
    print('OUT', os.path.getsize(OUT))
else:
    print(r.stderr[-500:].encode('ascii','replace').decode('ascii'))
