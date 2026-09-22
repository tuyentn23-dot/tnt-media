import os
from PIL import Image, ImageDraw, ImageFont
ROOT='.'
COVER='assets/youaremyonlyone_cover.png'
THUMB='output/vile_youaremyonlyone_thumb.jpg'
FONT='C:/Windows/Fonts/arialbd.ttf'
im=Image.open(COVER).convert('RGB')
# fit 1280x720: nen blur + bia giua
from PIL import ImageFilter
bg=im.resize((1280,720)).filter(ImageFilter.GaussianBlur(25))
fg=im.copy()
fg.thumbnail((700,650))
bg.paste(fg, ((1280-fg.width)//2,(720-fg.height)//2))
d=ImageDraw.Draw(bg)
f1=ImageFont.truetype(FONT,52)
f2=ImageFont.truetype(FONT,28)
title='You Are My Only One'
sub='Nh\u1ea1c Tr\u1eef T\u00ecnh - ViLe Vi'
def ctr(t,f,y,fill):
    bb=d.textbbox((0,0),t,font=f); w=bb[2]-bb[0]; x=(1280-w)//2
    d.text((x,y),t,font=f,fill=fill,stroke_width=3,stroke_fill='black')
ctr(title,f1,600,'white')
ctr(sub,f2,670,'#ffd700')
bg.save(THUMB,quality=92)
print('thumb', os.path.exists(THUMB), os.path.getsize(THUMB))
