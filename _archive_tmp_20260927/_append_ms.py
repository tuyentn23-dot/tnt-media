# append make_scene_v2 - khong dung moviepy resize

def make_scene(cpath, text, color, fs, dur, y, seed=0):
	from ops.compat import get_video_clip, concat as cc
	from ops.compat import _editor as _cmp_editor
	ColorClip = _cmp_editor()[5]
	from moviepy.video.VideoClip import VideoClip
	from PIL import Image
	import numpy as np
	V = get_video_clip()
	col = (255, 255, 0) if color == 'yellow' else ((0, 255, 204) if color == '#00ffcc' else (255, 255, 255))
	overlay = text_frame(text, fs, col, 720, 1280, y)
	if not isinstance(overlay, Image.Image):
		overlay = Image.fromarray(overlay).convert('RGBA')
	if cpath:
		_c = V(cpath)
	else:
		_c = ColorClip((720, 1280), color=(8, 10, 25), duration=dur)
	def mk(get, t):
		fr = get(t)
		img = Image.fromarray(fr.astype('uint8')).convert('RGBA')
		if img.size != (720, 1280):
			img = img.resize((720, 1280), Image.LANCZOS)
		img = Image.alpha_composite(img, overlay)
		return np.array(img.convert('RGB'))
	vid = VideoClip(lambda t: mk(_c.get_frame, t))
	vid = (vid.with_duration(dur).with_fps(30) if hasattr(vid, 'with_fps') else vid.set_fps(30).set_duration(dur))
	return vid
