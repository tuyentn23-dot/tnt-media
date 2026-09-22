# MoviePy v2 compatibility shim
import os
_local_ff = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "ffmpeg.exe")
if os.path.exists(_local_ff) and not os.environ.get("IMAGEIO_FFMPEG_EXE"):
	os.environ["IMAGEIO_FFMPEG_EXE"] = _local_ff

try:
	from PIL import Image
	if not hasattr(Image, "ANTIALIAS"):
		Image.ANTIALIAS = Image.LANCZOS
except Exception:
	pass


def _editor():
	try:
		from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip, ImageClip
		return VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip, ImageClip
	except Exception:
		from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip, ImageClip
		return VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip, ImageClip


def get_video_clip():
	return _editor()[0]


def get_audio_clip():
	return _editor()[1]


def concat(clips):
	cc = _editor()[4]
	return cc(clips, method="compose")


def composite(clips):
	CC = _editor()[3]
	return CC(clips)


def get_image_clip():
	return _editor()[6]


def text_clip(t, fs=48, color="white", font=None, size=None, method="caption"):
	TC = _editor()[2]
	kw = {}
	if font:
		kw["font"] = font
	return TC(t, fontsize=fs, color=color, stroke_color="black", stroke_width=4, size=size, method=method, align="center", **kw)


def color_clip(size, color, duration):
	CC = _editor()[5]
	return CC(size, color=color, duration=duration)



# Shim: moviepy 1.x dung set, 2.x dung with_. Gan alias with_* -> set_* tren base Clip.
def installwithshim():
    pairs = ['duration', 'position', 'start', 'end', 'audio', 'fps', 'size', 'opacity', 'mask', 'subclip', 'speed', 'volume', 'margin', 'resize', 'crop', 'rotate', 'image']
    targets = []
    try:
        from moviepy.Clip import Clip as BaseClip
        targets.append(BaseClip)
    except Exception:
        pass
    try:
        import moviepy.editor as me
        for cn in ['VideoFileClip','ImageClip','ColorClip','TextClip','CompositeVideoClip','VideoClip','AudioFileClip','AudioClip']:
            cc = getattr(me, cn, None)
            if cc is not None:
                targets.append(cc)
    except Exception:
        pass
    for cls in targets:
        for nm in pairs:
            wname = 'with'+chr(95)+nm
            sname = 'set'+chr(95)+nm
            if (not hasattr(cls, wname)) and hasattr(cls, sname):
                try:
                    setattr(cls, wname, getattr(cls, sname))
                except Exception:
                    pass
try:
    installwithshim()
except Exception:
    pass
