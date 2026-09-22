# content_video2.py - FIXED: correct font + topic footage + effects
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, "memory", "content_db.json")
FONT = "C:/Windows/Fonts/arialbd.ttf"

def load(kind):
    return json.load(open(DB, encoding="utf-8"))[kind]

def tts(text, out):
    from gtts import gTTS
    gTTS(text=text, lang="vi").save(out)
    return out

def best_bg(topic):
    import glob
    d = os.path.join(ROOT, "library", topic)
    fs = [f for f in glob.glob(os.path.join(d, "*.mp4")) if not os.path.basename(f).startswith("_")]
    return fs[0] if fs else None

def build(item, out):
    from ops.compat import get_video_clip, get_audio_clip
    from moviepy import TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips as cc
    V = get_video_clip(); A = get_audio_clip()
    vo = os.path.join(ROOT, "output", "vo2.mp3")
    tts(item["hook"]+" "+item["body"]+" "+item["payoff"], vo)
    aud = A(vo); dur = aud.duration + 0.5
    bg = best_bg(item["topic"])
    base = V(bg).resized(height=1280) if bg else ColorClip((720,1280), color=(8,10,25), duration=dur)
    base = base.cropped(width=720, x_center=base.w/2) if base.w>=720 else base.resized(width=720)
    if base.duration < dur:
        base = cc([base]*(int(dur/base.duration)+1)).subclipped(0, dur)
    else:
        base = base.subclipped(0, dur)
    def txt(t, fs, color):
        return TextClip(text=t, font=FONT, font_size=fs, color=color, stroke_color="black", stroke_width=4, size=(660,None), method="caption", text_align="center")
    hook = txt(item["hook"], 56, "yellow").with_position(("center",300)).with_duration(dur)
    pay = txt(item["payoff"], 44, "white").with_position(("center",760)).with_start(3).with_duration(dur-3)
    final = CompositeVideoClip([base, hook, pay]).with_audio(aud)
    final.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out

if __name__ == "__main__":
    print("loaded", len(load("whatif")))
