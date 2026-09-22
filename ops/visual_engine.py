# visual_engine.py - Ken Burns + grade + vignette + caption + progress (flat)
import os, math, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ops import voice_engine as VE
ROOT = VE.ROOT
FONT = os.path.join(ROOT, 'tools', 'font.ttf')

def _font(fs):
 return ImageFont.truetype(FONT, fs) if os.path.exists(FONT) else ImageFont.load_default()

def _wrap(text, fs, maxw):
 cw = max(6, int(maxw / (fs * 0.5)))
 return textwrap.wrap(text, width=cw) or ['']

def ken_burns(frame, t, dur, zoom0=1.0, zoom1=1.12, pan=(0.0, 0.0)):
 h, w = frame.shape[:2]
 z = zoom0 + (zoom1 - zoom0) * (t / max(dur, 0.001))
 nw, nh = int(w * z), int(h * z)
 img = Image.fromarray(frame).resize((nw, nh), Image.LANCZOS)
 cx = max(0, min(int((nw - w) / 2 + pan[0] * (nw - w) / 2), nw - w))
 cy = max(0, min(int((nh - h) / 2 + pan[1] * (nh - h) / 2), nh - h))
 return np.array(img.crop((cx, cy, cx + w, cy + h)))

def color_grade(frame, contrast=1.08, sat=1.12, warm=6):
 f = frame.astype(np.float32)
 f = (f - 128.0) * contrast + 128.0
 gray = f.mean(axis=2, keepdims=True)
 f = gray + (f - gray) * sat
 f[:, :, 0] += warm
 f[:, :, 2] -= warm * 0.5
 return np.clip(f, 0, 255).astype(np.uint8)

def vignette(frame, strength=0.28):
 h, w = frame.shape[:2]
 yy, xx = np.mgrid[0:h, 0:w]
 dx = (xx - w / 2) / (w / 2)
 dy = (yy - h / 2) / (h / 2)
 d = np.sqrt(dx * dx + dy * dy)
 mask = np.clip(1 - strength * (d ** 2), 0, 1)[..., None]
 return (frame.astype(np.float32) * mask).astype(np.uint8)

def caption_layer(text, W, H, fs=52, y_ratio=0.72, color=(255, 255, 255)):
 img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
 dr = ImageDraw.Draw(img)
 font = _font(fs)
 body = chr(10).join(_wrap(text, fs, W - 120))
 y = int(H * y_ratio)
 dr.multiline_text((W / 2 + 3, y + 3), body, font=font, fill=(0, 0, 0, 200), anchor='ma', align='center', spacing=int(fs * 0.25))
 dr.multiline_text((W / 2, y), body, font=font, fill=color + (255,), anchor='ma', align='center', spacing=int(fs * 0.25), stroke_width=4, stroke_fill=(0, 0, 0, 255))
 return np.array(img)

def progress_bar(W, frac, h=8, color=(233, 69, 96)):
 img = Image.new('RGBA', (W, h), (0, 0, 0, 90))
 dr = ImageDraw.Draw(img)
 dr.rectangle([0, 0, int(W * max(0.0, min(1.0, frac))), h], fill=color + (255,))
 return np.array(img)
