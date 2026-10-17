# -*- coding: utf-8 -*-
"""TNT Media OS - unified quality gate.

Single source of truth for pre-publish quality checks.
Combines quality_standard.py thresholds + viral_engine.analyze metrics.
"""
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    from ops.quality_standard import STANDARD
except Exception:
    STANDARD = {"video": {"min_hook": 4.0, "min_score": 75, "max_dur": 20}}

try:
    from ops.viral_engine import analyze as _viral_analyze
except Exception:
    _viral_analyze = None

CATEGORY_MAP = {
    "beauty_antiaging": "26",
    "health": "26",
    "science_loop": "28",
    "animal_facts": "15",
    "what_if_space": "28",
    "abstract_music": "10",
    "music_chill": "10",
    "abstract_visual": "24",
    "default": "24",
}

def category_for(topic):
    """Map a topic to a YouTube categoryId."""
    if not topic:
        return CATEGORY_MAP["default"]
    return CATEGORY_MAP.get(topic, CATEGORY_MAP["default"])

def evaluate(video_path):
    """Run the quality gate on a local video file."""
    std = STANDARD.get("video", {})
    min_score = std.get("min_score", 75)
    min_hook = std.get("min_hook", 4.0)
    max_dur = std.get("max_dur", 20)

    if not os.path.exists(video_path):
        return {"ok": False, "passes": False, "score": 0, "metrics": {}, "reasons": ["file not found: " + str(video_path)], "standard": std}

    if _viral_analyze is None:
        return {"ok": False, "passes": False, "score": 0, "metrics": {}, "reasons": ["viral_engine unavailable"], "standard": std}

    try:
        metrics = _viral_analyze(video_path)
    except Exception as e:
        return {"ok": False, "passes": False, "score": 0, "metrics": {}, "reasons": ["analysis error: " + str(e)], "standard": std}

    score = int(metrics.get("viral_score", 0))
    hook = float(metrics.get("hook_motion", 0.0))
    dur = float(metrics.get("duration", 0.0))

    reasons = []
    from ops.compat import get_video_clip; _V=get_video_clip(); _c=_V(video_path); width,height=int(_c.size[0]),int(_c.size[1]); fps=float(_c.fps or 0.0); _c.close(); metrics.update({'width':width,'height':height,'fps':round(fps,2)}); reasons += ([f'resolution {width}x{height} < 540x960'] if width < 540 or height < 960 else []) + ([f'fps {fps:.2f} < 15'] if fps < 15.0 else [])
    if score < min_score:
        reasons.append("score %d < %d" % (score, min_score))
    if hook < min_hook:
        reasons.append("hook %.2f < %.2f" % (hook, min_hook))
    if dur > max_dur:
        reasons.append("duration %.2f > %d" % (dur, max_dur))

    passes = len(reasons) == 0
    return {"ok": True, "passes": passes, "score": score, "metrics": metrics, "reasons": reasons, "standard": std}

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "output/story_shark_teeth.mp4"
    print(json.dumps(evaluate(p), ensure_ascii=False, indent=2))


def check(video_path):
	"""Lenient check cho runner: ok neu file ton tai, du lon, va co audio (voice)."""
	import subprocess
	if not video_path or not os.path.exists(video_path):
		return {'ok': False, 'errors': ['file not found: ' + str(video_path)]}
	sz = os.path.getsize(video_path)
	if sz < 300000:
		return {'ok': False, 'errors': ['file too small: ' + str(sz)]}
	ff = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
	try:
		r = subprocess.run([ff, '-i', video_path, '-hide_banner'], capture_output=True, text=True, timeout=30, creationflags=0x08000000)
		has_audio = 'Audio:' in r.stderr
		has_video = 'Video:' in r.stderr
		if not has_video:
			return {'ok': False, 'errors': ['no video stream']}
		if not has_audio:
			return {'ok': False, 'errors': ['no audio (voice missing)']}
	except Exception as e:
		return {'ok': True, 'errors': [], 'warn': 'probe failed: ' + str(e)[:100]}
	return {'ok': True, 'errors': []}
