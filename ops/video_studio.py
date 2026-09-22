# video_studio.py - high-quality short renderer (flat, no deep blocks)
from ops import voice_engine as VE
import os, sys, json, math, random, hashlib
import numpy as np
from ops import visual_engine as VX
from ops import voice_synth as VS
from ops import voice_master as VM
from ops import hook_engine as HE
from ops.compat import get_video_clip, get_audio_clip, concat as cc

W, H = 720, 1280
FPS = 30

def _listdir(d):
 return sorted(os.listdir(d)) if os.path.isdir(d) else []

def _mp4s(d, skip_music=True):
 fs = [f for f in _listdir(d) if f.lower().endswith('.mp4')]
 return [f for f in fs if not (skip_music and f.startswith('music'))]

def _topic_footage(topic, seed):
 lib = os.path.join(VE.ROOT, 'library')
 d = os.path.join(lib, str(topic).strip().lower())
 files = [os.path.join(d, f) for f in _mp4s(d)]
 subs = _listdir(lib)
 allf = [os.path.join(lib, s, f) for s in subs for f in _mp4s(os.path.join(lib, s))]
 pool = files or allf
 random.seed(seed)
 random.shuffle(pool)
 return pool

def _fit(frame, w=W, h=H):
 img = Image.fromarray(frame)
 r = max(w / img.width, h / img.height)
 img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
 x = (img.width - w) // 2
 y = (img.height - h) // 2
 return np.array(img.crop((x, y, x + w, y + h)))

from PIL import Image

def _kb_grade(frame, t, dur, seed):
 rnd = random.Random(seed)
 z0 = 1.0 + rnd.random() * 0.05
 z1 = z0 + 0.08 + rnd.random() * 0.08
 px = (rnd.random() - 0.5) * 0.6
 py = (rnd.random() - 0.5) * 0.6
 f = VX.ken_burns(frame, t, dur, z0, z1, (px, py))
 f = VX.color_grade(f)
 f = VX.vignette(f)
 return f
def _mk_frame(t, base, bd, capf, caf, dur, seed):
 fr = base.get_frame(t % bd)
 fr = _fit(fr)
 fr = _kb_grade(fr, t, dur, seed)
 out = fr.astype(np.float32) * (1 - caf) + capf[..., :3] * caf
 out = np.clip(out, 0, 255).astype(np.uint8)
 frac = min(1.0, max(0.0, t / max(dur, 0.001)))
 bw = int(out.shape[1] * frac)
 out[-8:, :bw] = np.array([233, 69, 96], 'uint8')
 return out

def _make_scene_clip(cpath, text, dur, seed, fs=54):
 from ops.compat import get_video_clip
 from moviepy.video.VideoClip import VideoClip, ColorClip
 V = get_video_clip()
 base = V(cpath) if (cpath and os.path.exists(cpath)) else ColorClip((W, H), color=(8, 10, 25), duration=dur)
 bd = base.duration or dur
 cap = VX.caption_layer(text, W, H, fs=fs, y_ratio=0.72)
 capf = cap.astype(np.float32)
 caf = capf[..., 3:4] / 255.0
 v = VideoClip(lambda t: _mk_frame(t, base, bd, capf, caf, dur, seed))
 v = v.set_duration(dur) if hasattr(v, 'set_duration') else v.with_duration(dur)
 v = v.set_fps(FPS) if hasattr(v, 'set_fps') else v.with_fps(FPS)
 return v
def split_text(item, n):
 full = (item.get('hook', '') + ' ' + item.get('body', '') + ' ' + item.get('payoff', '')).strip()
 import re
 parts = [p.strip() for p in re.split(r'[.!?;]+', full) if p.strip()]
 parts = parts or [full]
 idx = [int(round(i * len(parts) / n)) for i in range(n)]
 idx = [min(x, len(parts) - 1) for x in idx]
 return [parts[idx[i]: (idx[i + 1] if i + 1 < n else len(parts))] for i in range(n)]

def render(item, out, voice='female_north', preset='hype', music=None, seed=None):
 from ops.compat import get_audio_clip, concat as cc
 cid = str(item.get('id', 'x'))
 seed = seed if seed is not None else int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
 od = os.path.join(VE.ROOT, 'output')
 os.makedirs(od, exist_ok=True)
 vo = os.path.join(od, 'vo' + cid + '.mp3')
 text_full = (item.get('hook', '') + ' ' + item.get('body', '') + ' ' + item.get('payoff', '')).strip()
 VS.synth(text_full, vo, voice=voice, preset=preset)
 dur = min(VM.duration(vo), 58.0)
 n = max(2, int(round(dur / 3.5)))
 texts = split_text(item, n)
 pool = _topic_footage(item.get('topic', ''), seed)
 scenes = [_make_scene_clip((pool[i % len(pool)] if pool else None), ' '.join(texts[i]), dur / n, seed + i) for i in range(n)]
 body = cc(scenes) if len(scenes) > 1 else scenes[0]
 aud = get_audio_clip()(vo)
 body = body.set_audio(aud) if hasattr(body, 'set_audio') else body.with_audio(aud)
 final_out = out
 body.write_videofile(final_out, fps=FPS, codec='libx264', audio_codec='aac', preset='medium', threads=4)
 return final_out
