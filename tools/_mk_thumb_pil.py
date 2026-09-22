# -*- coding: utf-8 -*-
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
LOOP = os.path.join(ROOT, 'assets', 'youtube_love_vinyl_dynamic_loop.mp4')
frame = os.path.join(ROOT, 'output', '_vinyl_frame.jpg')
THUMB = os.path.join(ROOT, 'output', 'vile_lang_im_thuong_anh_thumb.jpg')
FONT = 'C:/Windows/Fonts/arialbd.ttf'

subprocess.run([FF,'-y','-ss','2','-i',LOOP,'-frames:v','1',frame], capture_output=True)
img = Image.open(frame).convert('RGB').resize((1280,720))
d = ImageDraw.Draw(img)
f1 = ImageFont.truetype(FONT, 60)
f2 = ImageFont.truetype(FONT, 32)
title = 'L\u1eb7ng Im Th\u01b0\u01a1ng Anh'
sub = 'Nh\u1ea1c Tr\u1eef T\u00ecnh - ViLe Vi'
# ve text can giua duoi
def center(text, font, y, fill):
    bb = d.textbbox((0,0), text, font=font)
    w = bb[2]-bb[0]
    x = (1280-w)//2
    d.text((x,y), text, font=font, fill=fill, stroke_width=3, stroke_fill='black')
center(title, f1, 500, 'white')
center(sub, f2, 585, '#ffd700')
img.save(THUMB, quality=92)
print('thumb', os.path.exists(THUMB), os.path.getsize(THUMB) if os.path.exists(THUMB) else 0)
