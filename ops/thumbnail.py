# thumbnail.py - auto thumbnail from best frame + big hook text (flat)
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
from ops import ffmpeg_render as FR
FFMPEG = FR.FFMPEG
ROOT = FR.ROOT
FONT = os.path.join(ROOT, 'tools', 'font.ttf')

def grab_frame(video, t, out):
 subprocess.run([FFMPEG, '-y', '-ss', str(t), '-i', video, '-frames:v', '1', out], capture_output=True, text=True)
 return out

 return out
def make(video, hook, out, t=None):
 dur = 15
 t = t if t is not None else dur * 0.4
 d = os.path.dirname(out)
 tmpf = os.path.join(d, '_thumb_src.png')
 grab_frame(video, t, tmpf)
 img = Image.open(tmpf).convert('RGB').resize((720, 1280), Image.LANCZOS)
 dr = ImageDraw.Draw(img)
 dr.rectangle([0, 0, 720, 420], fill=(0, 0, 0))
 font = ImageFont.truetype(FONT, 64)
 import textwrap
 lines = textwrap.wrap(hook, width=18)[:3]
 ys = [60 + i * 90 for i in range(len(lines))]
 _ = [dr.text(((720 - dr.textlength(ln, font=font)) / 2, ys[i]), ln, font=font, fill=(255, 235, 59), stroke_width=5, stroke_fill=(0, 0, 0)) for i, ln in enumerate(lines)]
 img.save(out)
 return out
