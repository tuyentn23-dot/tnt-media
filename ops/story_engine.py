# story_engine.py - viral story shorts: TTS voice + footage + topic music
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
STORY_DB = os.path.join(ROOT, "memory", "story_db.json")

def load_stories():
    return json.load(open(STORY_DB, encoding="utf-8"))["stories"]

def tts(text, out):
    from gtts import gTTS
    gTTS(text=text, lang="vi").save(out)
    return out

def voiceover(story, out):
    text = story["hook"] + " " + story["body"] + " " + story["payoff"]
    return tts(text, out)
def overlay_captions(clip, story):
    from moviepy import TextClip, CompositeVideoClip
    from ops.captions import wrap
    txt = wrap(story["hook"] + " " + story["body"] + " " + story["payoff"], 20)
    try:
        tc = TextClip(text=txt, font_size=46, color="white", stroke_color="black", stroke_width=3, size=(int(clip.w*0.9), None), method="caption")
        tc = tc.with_position(("center","center")).with_duration(clip.duration)
        return CompositeVideoClip([clip, tc])
    except Exception as e:
        print("caption fail", e)
        return clip
def build(story, footage, music, out):
    from ops.compat import get_video_clip, get_audio_clip
    V = get_video_clip()
    A = get_audio_clip()
    vo = os.path.join(ROOT, "library", "vo_"+story["id"]+".mp3")
    voiceover(story, vo)
    aud = A(vo)
    dur = aud.duration + 0.4
    c = V(footage)
    if c.duration > dur:
        c = c.subclipped(0, dur)
    c = overlay_captions(c, story).with_audio(aud)
    c.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out

if __name__ == "__main__":
    ss = load_stories()
    print("loaded", len(ss))
