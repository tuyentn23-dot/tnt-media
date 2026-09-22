# content_video.py - build what-if/fact shorts: voiceover + big captions + bg
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, "memory", "content_db.json")

def load(kind):
    d = json.load(open(DB, encoding="utf-8"))
    return d[kind]

def tts(text, out):
    from gtts import gTTS
    gTTS(text=text, lang="vi").save(out)
    return out

def build(item, bg, out):
    from ops.compat import get_video_clip, get_audio_clip
    from moviepy import TextClip, CompositeVideoClip, ColorClip
    V = get_video_clip()
    A = get_audio_clip()
    vo = os.path.join(ROOT, "output", "vo.mp3")
    tts(item["hook"] + " " + item["body"] + " " + item["payoff"], vo)
    aud = A(vo)
    dur = aud.duration + 0.5
    base = V(bg).resized(height=1280).cropped(width=720, x_center=360) if os.path.exists(bg) else ColorClip((720,1280), color=(10,10,20), duration=dur)
    if base.duration < dur:
        from moviepy import concatenate_videoclips as cc
        reps = int(dur/base.duration)+1
        base = cc([base]*reps).subclipped(0, dur)
    else: base = base.subclipped(0, dur)
    txt = item["hook"] + chr(10)+chr(10) + item["payoff"]
    tc = TextClip(text=txt, font_size=52, color="white", stroke_color="black", stroke_width=4, size=(640,None), method="caption", text_align="center")
    tc = tc.with_position(("center","center")).with_duration(dur)
    final = CompositeVideoClip([base, tc]).with_audio(aud)
    final.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out

if __name__ == "__main__":
    print("loaded whatif:", len(load("whatif")))
