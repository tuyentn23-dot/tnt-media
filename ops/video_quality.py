# -- coding: utf-8 --
"""TNT Media OS - video quality builder (P7).

Builds high-retention shorts: strong hook card, word-timed captions,
safe-area text, crossfade transitions, vignette + optional background music.
Uses PIL for text rendering (stable) and ops.compat for MoviePy v1/v2.
"""
import os
import sys
import math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"
W, H = 1080, 1920
SAFE_TOP = 280
SAFE_BOTTOM = 420

def _pil_text(text, font_path, size, color=(255,255,255), stroke=6, stroke_color=(0,0,0), max_w=920, align="center"):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    font = ImageFont.truetype(font_path, size) if os.path.exists(font_path) else ImageFont.load_default()
    words = str(text).split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_w or not cur:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    lh = size + int(size * 0.35)
    img_w = max_w + stroke * 4
    img_h = lh * len(lines) + stroke * 4
    img = Image.new("RGBA", (img_w, img_h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    y = stroke * 2
    for ln in lines:
        bbox = font.getbbox(ln)
        tw = bbox[2] - bbox[0]
        x = (img_w - tw) // 2 if align == "center" else stroke * 2
        d.text((x, y), ln, font=font, fill=color, stroke_width=stroke, stroke_fill=stroke_color)
        y += lh
    return np.array(img)

def _to_frame(np_img):
    from moviepy.editor import ImageClip
    return ImageClip(np_img)

def _fit(clip, w=1080, h=1920):
    r = clip.resize(height=h) if hasattr(clip, "resize") else clip.resized(height=h)
    x = max(0, (r.w - w) // 2); y = max(0, (r.h - h) // 2)
    cr = r.cropped(x1=x, y1=y, width=w, height=h) if hasattr(r, "cropped") else r.crop(x1=x, y1=y, width=w, height=h)
    return cr

def _xfade(a, b, d=0.3):
    try:
        from moviepy import CompositeVideoClip
        return CompositeVideoClip([a, b.with_start(a.duration - d).crossfadein(d)]).with_duration(a.duration + b.duration - d)
    except Exception:
        from ops.compat import concat
        return concat([a, b])

def build_short(footage_paths, script_lines, out_path, hook_text=None, music_path=None, target_dur=15.0, voice_text=None, voice_path=None, sentences=None, voice_name=None):
    "Delegate to ops.video_build (quality pipeline)."
    from ops.video_build import build_short as _bs
    return _bs(footage_paths, script_lines, out_path, hook_text=hook_text, music_path=music_path, target_dur=target_dur, voice_text=voice_text, voice_path=voice_path, sentences=sentences, voice_name=voice_name)

def rank_footage(paths, top=None, max_scan=12):
    """Score footage by hook_motion (cached, capped scan). Best-first."""
    try:
        from ops.viral_engine import analyze
    except Exception:
        analyze = None
    cache = _load_cache()
    scored = []
    scanned = 0
    for p in paths:
        sc = cache.get(p)
        if sc is None and analyze and scanned < max_scan:
            try:
                m = analyze(p); sc = int(m.get("viral_score", 0))
            except Exception:
                sc = 0
            cache[p] = sc
            _save_cache(cache)
            scanned += 1
        scored.append((sc or 0, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    out = [p for sc, p in scored]
    return out[:top] if top else out
def _load_cache():
    try:
        import json
        if os.path.exists(CACHE_PATH):
            return json.load(open(CACHE_PATH, encoding="utf-8"))
    except Exception:
        pass
    return {}

def _save_cache(c):
    try:
        import json
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        json.dump(c, open(CACHE_PATH, "w", encoding="utf-8"))
    except Exception:
        pass
