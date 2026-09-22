import os
os.environ.setdefault("IMAGEIO_FFMPEG_EXE", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"tools","ffmpeg.exe"))
# make_story_video.py - video story nghiem tuc
import os, sys, json, glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
LIB=os.path.join(ROOT,"library")
OUT=os.path.join(ROOT,"output")
FONT="C:/Windows/Fonts/arialbd.ttf"
TARGET=15.0
FOOT={"shark":"shark","animal":"animal","space":"space","ocean":"ocean","insect":"spider"}
def clips(folder):
    return sorted(glob.glob(os.path.join(LIB,folder,"*.mp4")))

def scene(foot, text, dur):
    from ops.compat import get_video_clip
    from moviepy import TextClip, CompositeVideoClip, concatenate_videoclips as cc
    V=get_video_clip()
    base=V(foot)
    if base.duration < dur: base=cc([base]*(int(dur/base.duration)+1))
    base=base.subclipped(0,dur).resized(height=1920)
    base=base.cropped(width=1080,height=1920,x_center=base.w/2,y_center=base.h/2)
    t=TextClip(text=text, font="C:/Windows/Fonts/arialbd.ttf", font_size=54, color="white", stroke_color="black", stroke_width=5, size=(960,None), method="caption").with_duration(dur).with_position(("center","center"))
    return CompositeVideoClip([base,t]).with_duration(dur)

def build(item, out):
    from gtts import gTTS
    from moviepy import concatenate_videoclips as cc, AudioFileClip
    folder=FOOT.get(item["topic"],"animal")
    cs=clips(folder)
    if not cs: cs=clips("abstract")
    txt=item["hook"]+" "+item["body"]+" "+item["payoff"]
    vo=os.path.join(OUT,"vo_story.mp3")
    gTTS(text=txt,lang="vi").save(vo)
    aud=AudioFileClip(vo)
    seg=TARGET/3.0
    parts=[("SƯ THẬT: "+item["hook"],0),(item["body"],1),(item["payoff"],2)]
    scenes=[]
    for tx,i in parts:
            scenes.append(scene(cs[i%len(cs)], tx, seg))
    final=cc(scenes).subclipped(0,TARGET)
    if aud.duration>TARGET: aud=aud.subclipped(0,TARGET)
    final=final.with_audio(aud)
    final.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out

if __name__=="__main__":
    import json as J
    db=J.load(open(os.path.join(ROOT,"memory","content_db.json"),encoding="utf-8"))
    fid=sys.argv[1] if len(sys.argv)>1 else "shark_teeth"
    item=[f for f in db["facts"] if f["id"]==fid][0]
    out=os.path.join(OUT,"story_"+fid+".mp4")
    print("building",fid)
    build(item,out)
    print("DONE",out)
