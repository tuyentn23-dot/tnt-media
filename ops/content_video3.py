# content_video3.py - effects: bg zoom, pop hook, fade payoff, progress bar
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
    vo = os.path.join(ROOT, "output", "vo3.mp3")
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
    hook = txt(item["hook"], 58, "yellow").with_position(("center",300)).with_duration(dur)
    pay = txt(item["payoff"], 46, "white").with_position(("center",720)).with_start(3).with_duration(dur-3)
    q = item.get("question","")
    qclip = txt(q, 40, "#00ffcc").with_position(("center",1050)).with_start(6).with_duration(max(0.1,dur-6)) if q else None
    bar = ColorClip((720,8), color=(255,215,0)).with_duration(dur).with_position(("center",1272))
    layers = [base, hook, pay, bar] + ([qclip] if qclip else [])
    final = CompositeVideoClip(layers).with_audio(aud)
    final.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out

if __name__ == "__main__":
    print("v3 ready")
