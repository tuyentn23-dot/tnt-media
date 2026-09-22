# -- coding: utf-8 --
"TNT Media OS - enhanced video builder (quality pass)."
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('IMAGEIO_FFMPEG_EXE', os.path.join(ROOT, 'tools', 'ffmpeg.exe'))
try:
    import ops.compat # noqa: F401 (sets IMAGEIO_FFMPEG_EXE)
except Exception:
    pass

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
W, H = 1080, 1920
SAFE_TOP = 300
SAFE_BOTTOM = 480
FPS = 30
CROSS = 0.35
ENCODE_PRESET = os.environ.get('TNT_ENC_PRESET', 'veryfast')
BITRATE = os.environ.get('TNT_BITRATE', '8000k')
AUDIO_BITRATE = os.environ.get('TNT_ABITRATE', '192k')

def _pil_text(text, size, color=(255,255,255), stroke=6, stroke_color=(0,0,0), max_w=920):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    fp = FONT_BOLD
    font = ImageFont.truetype(fp, size) if os.path.exists(fp) else ImageFont.load_default()
    words = str(text).split()
    lines = []
    cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        bb = font.getbbox(t)
        if bb[2] - bb[0] <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    lh = size + int(size * 0.4)
    pad = stroke * 4
    iw = max_w + pad
    ih = lh * len(lines) + pad
    img = Image.new("RGBA", (iw, ih), (0,0,0,0))
    d = ImageDraw.Draw(img)
    y = stroke * 2
    for ln in lines:
        bb = font.getbbox(ln)
        tw = bb[2] - bb[0]
        x = (iw - tw) // 2
        d.text((x, y), ln, font=font, fill=color, stroke_width=stroke, stroke_fill=stroke_color)
        y += lh
    return np.array(img)

def _to_frame(a):
    try:
        from moviepy.editor import ImageClip
    except Exception:
        from moviepy import ImageClip
    return ImageClip(a)

def _vignette_np():
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W]
    cx = W / 2.0
    cy = H / 2.0
    d = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    m = np.clip(d - 0.55, 0, 1.4) / 1.4
    al = (m * 210).astype('uint8')
    out = np.zeros((H, W, 4), dtype='uint8')
    out[:, :, 3] = al
    return out

def _crop(clip, x1, y1, width, height):
    m = getattr(clip, "cropped", None)
    if m is not None:
        return m(x1=x1, y1=y1, width=width, height=height)
    return clip.crop(x1=x1, y1=y1, width=width, height=height)

def _fit(clip, w=W, h=H):
    sw = int(clip.w)
    sh = int(clip.h)
    _resize = getattr(clip, "resized", None) or getattr(clip, "resize", None)
    if sw >= w and sh >= h:
        try:
            r = _resize(height=h, resample="lanczos")
        except Exception:
            r = _resize(height=h)
        x = max(0, (r.w - w) // 2)
        y = max(0, (r.h - h) // 2)
        return _crop(r, x, y, w, h)
def _xfade(a, b, d=CROSS):
    try:
        from moviepy.editor import CompositeVideoClip
        return CompositeVideoClip([a, b.with_start(a.duration - d).crossfadein(d)]).with_duration(a.duration + b.duration - d)
    except Exception:
        from ops.compat import concat
        return concat([a, b])

def build_short(footage_paths, script_lines, out_path, hook_text=None, music_path=None, target_dur=15.0, voice_text=None, voice_path=None, sentences=None, voice_name=None):
    "Delegate to ops.video_build2 (flatten fast pipeline)."
    from ops.video_build2 import build_short as _bs2
    return _bs2(footage_paths, script_lines, out_path, hook_text=hook_text, music_path=music_path, target_dur=target_dur, voice_text=voice_text, voice_path=voice_path, sentences=sentences, voice_name=voice_name)

