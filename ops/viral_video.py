# viral_video.py - video chuan viral
import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
os.environ.setdefault("IMAGEIO_FFMPEG_EXE", os.path.join(ROOT,"tools","ffmpeg.exe"))
FONT="C:/Windows/Fonts/arialbd.ttf"
W,H=1080,1920
def make(hook,body,payoff,footage,out):
    from moviepy import TextClip, CompositeVideoClip
    from ops.compat import get_video_clip
    V=get_video_clip()
    c=V(footage)
    if c.w<W or c.h<H: c=c.resized(height=H)
    c=c.cropped(width=W,height=H,x_center=c.w//2,y_center=c.h//2)
    dur=min(15,c.duration)
    c=c.subclipped(0,dur)
    seg=dur/3
    def txt(t,fs,col,y):
        return TextClip(text=t,font=FONT,font_size=fs,color=col,stroke_color="black",stroke_width=6,size=(W-100,None),method="caption").with_position(("center",y)).with_duration(seg)
    t1=txt(hook,70,"yellow",300)
    t2=txt(body,62,"white",H//2-100).with_start(seg)
    t3=txt(payoff,66,"#00ffcc",H-650).with_start(2*seg)
    final=CompositeVideoClip([c,t1,t2,t3]).with_duration(dur)
    final.write_videofile(out,codec="libx264",fps=30,preset="medium")
    return out
