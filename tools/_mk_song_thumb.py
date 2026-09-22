# -*- coding: utf-8 -*-
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
LOOP = os.path.join(ROOT, 'assets', 'youtube_love_vinyl_dynamic_loop.mp4')
THUMB = os.path.join(ROOT, 'output', 'vile_lang_im_thuong_anh_thumb.jpg')
FONT = 'C:/Windows/Fonts/arialbd.ttf'
TITLE = 'L\u1eb7ng Im Th\u01b0\u01a1ng Anh'
SUB = 'Nh\u1ea1c Tr\u1eef T\u00ecnh' 

# 1) lay 1 frame tu vinyl loop lam anh bia dia nhac
frame = os.path.join(ROOT, 'output', '_vinyl_frame.jpg')
subprocess.run([FF,'-y','-ss','2','-i',LOOP,'-frames:v','1',frame], capture_output=True)
print('frame', os.path.exists(frame))

# 2) dung ffmpeg drawtext tao thumbnail 1280x720
# ve ten bai hat + phu de, chu lon, vien den
fc = (
 "scale=1280:720,"
 "drawtext=fontfile='"+FONT+"':text='"+TITLE+"':fontcolor=white:fontsize=64:borderw=4:bordercolor=black:x=(w-text_w)/2:y=h-200,"
 "drawtext=fontfile='"+FONT+"':text='"+SUB+"':fontcolor=#ffd700:fontsize=36:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h-120"
)
cmd=[FF,'-y','-i',frame,'-vf',fc,'-frames:v','1',THUMB]
r=subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('thumb rc', r.returncode)
print('thumb', os.path.exists(THUMB), os.path.getsize(THUMB) if os.path.exists(THUMB) else 0)
if r.returncode!=0:
    print(r.stderr[-400:].encode('ascii','replace').decode('ascii'))
