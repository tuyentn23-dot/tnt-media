# make_music_video.py - nhac Viet hoa: footage + nhac + lyric
import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
TARGET=15.0
def build(footage, music, out):
    from ops.compat import get_video_clip, get_audio_clip
    V=get_video_clip()
    A=get_audio_clip()
    aud=A(music)
    dur=min(TARGET, aud.duration)
    c=V(footage)
    if c.duration < dur:
        from moviepy import concatenate_videoclips as cc
        c=cc([c]*(int(dur/c.duration)+1))
    c=c.subclipped(0,dur).resized(height=1920)
    c=c.cropped(width=1080, height=1920, x_center=c.w/2, y_center=c.h/2)
    c=c.with_audio(aud.subclipped(0,dur))
    c.write_videofile(out, codec="libx264", audio_codec="aac", fps=30, preset="medium")
    return out
if __name__=="__main__":
    f=sys.argv[1]; m=sys.argv[2]; o=sys.argv[3]
    print(build(f,m,o))
