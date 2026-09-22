# content_video4.py - MULTI-SCENE story video (real, not slideshow)
# Each scene = different footage clip + its own text, synced to narration parts
import os, sys, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, "memory", "content_db.json")
FONT = "C:/Windows/Fonts/arialbd.ttf"

def load(kind):
    return json.load(open(DB, encoding="utf-8"))[kind]

def clips(topic):
    d = os.path.join(ROOT, "library", topic)
    fs = [f for f in glob.glob(os.path.join(d, "*.mp4")) if not os.path.basename(f).startswith("_")]
    return fs if fs else []

def tts(text, out):
    from gtts import gTTS
    gTTS(text=text, lang="vi").save(out)
    return out

def txt(t, fs, color):
    from moviepy import TextClip
    return TextClip(text=t, font=FONT, font_size=fs, color=color, stroke_color="black", stroke_width=4, size=(660,None), method="caption", text_align="center")

def build(item, out):
    from ops.compat import get_video_clip, get_audio_clip
    from moviepy import CompositeVideoClip, concatenate_videoclips as cc
    V = get_video_clip(); A = get_audio_clip()
    parts = [item["hook"], item["body"], item["payoff"]]
    colors = ["yellow","white","#00ffcc"]
    sizes = [58, 46, 48]
    vo = os.path.join(ROOT, "output", "vo4.mp3")
    tts(" ".join(parts), vo)
    aud = A(vo); total = aud.duration + 0.4
    seg = total / 3.0
    cs = clips(item["topic"])
    scenes = []
    for i in range(3):
        cpath = cs[i % len(cs)] if cs else None
        base = V(cpath).resized(height=1280) if cpath else None
        base = base.cropped(width=720, x_center=base.w/2) if base else None
        if base.duration < seg: base = cc([base]*(int(seg/base.duration)+1))
        base = base.subclipped(0, seg)
        t = txt(parts[i], sizes[i], colors[i]).with_position(("center","center")).with_duration(seg)
        scenes.append(CompositeVideoClip([base, t]).with_duration(seg))
    final = cc(scenes).with_audio(aud)
    final.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out

if __name__ == "__main__":
    print("v4 renderer ready")
