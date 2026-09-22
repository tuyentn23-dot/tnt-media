# make_full.py
import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
os.environ.setdefault("IMAGEIO_FFMPEG_EXE", os.path.join(ROOT,"tools","ffmpeg.exe"))
def build(footage, voice_text, out):
    from gtts import gTTS
    from moviepy import VideoFileClip, AudioFileClip
    vo=os.path.join(ROOT,"output/vo.mp3")
    gTTS(text=voice_text,lang="vi").save(vo)
    aud=AudioFileClip(vo)
    vid=VideoFileClip(footage)
    dur=min(15, aud.duration, vid.duration)
    vid=vid.subclipped(0,dur)
    vid=vid.resized(lambda t: 1.0+(0.15*t)/dur)
    vid=vid.cropped(width=1080,height=1920,x_center=vid.w//2,y_center=vid.h//2)
    vid=vid.with_audio(aud.subclipped(0,vid.duration))
    vid.write_videofile(out,codec="libx264",audio_codec="aac",fps=30,preset="medium")
    return out
