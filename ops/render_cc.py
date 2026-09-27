import os, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
BG = (12, 10, 30)
FG = (255, 255, 255)
ACCENT = (255, 90, 180)


def _font(size):
 for p in [
 'C:/Windows/Fonts/arialbd.ttf',
 'C:/Windows/Fonts/arial.ttf',
 '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
 ]:
 if os.path.exists(p):
 try:
 return ImageFont.truetype(p, size)
 except Exception:
 pass
 return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
 words = text.split()
 lines, cur = [], ''
 for w in words:
 t = (cur + ' ' + w).strip()
 if draw.textlength(t, font=font) <= max_w:
 cur = t
 else:
 if cur:
 lines.append(cur)
 cur = w
 if cur:
 lines.append(cur)
 return lines


def make_text_card(text, out_path, tag=None):
 img = Image.new('RGB', (W, H), BG)
 d = ImageDraw.Draw(img)
 # top accent bar
 d.rectangle([0, 0, W, 14], fill=ACCENT)
 d.rectangle([0, H - 14, W, H], fill=ACCENT)

 if tag:
 tf = _font(48)
 d.text((60, 80), tag.upper(), font=tf, fill=ACCENT)

 font = _font(88)
 lines = _wrap(d, text or '', font, W - 140)
 total_h = len(lines) * 110
 y = (H - total_h) // 2
 for ln in lines:
 w = d.textlength(ln, font=font)
 d.text(((W - w) // 2, y), ln, font=font, fill=FG)
 y += 110
 img.save(out_path, 'JPEG', quality=90)
 return out_path


def render_slideshow(cards, out_path, per_card=3.0, bgm=None):
 '''cards: list of image paths. Renders mp4 with ffmpeg concat demuxer.'''
 out_path = str(out_path)
 d = os.path.dirname(out_path)
 listfile = os.path.join(d, '_concat.txt')
 with open(listfile, 'w', encoding='utf-8') as f:
 for i, c in enumerate(cards):
 f.write(f"file '{Path(c).as_posix()}'
duration {per_card}
")
 f.write(f"file '{Path(cards[-1]).as_posix()}'
")

 cmd = [
 FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', listfile,
 '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p',
 '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
 out_path,
 ]
 r = subprocess.run(cmd, capture_output=True)
 if r.returncode != 0:
 raise RuntimeError('ffmpeg failed: ' + r.stderr.decode('utf-8', 'ignore')[-500:])
 return out_path
