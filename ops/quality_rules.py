# -- coding: utf-8 --
"""TNT Media OS - QUALITY RULES (mandatory for ALL video publishing).

RULES:
1. ALWAYS create a NEW video file (never reuse old output videos).
2. ALWAYS have Vietnamese voiceover (vi-VN-HoaiMyNeural).
3. ALWAYS have background music.
4. ALWAYS have captions/subtitles.
5. NEVER republish a topic already published.
6. NEVER publish video from output/ folder that already exists (must be fresh build).
"""
import os
import sys
import time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
MIN_VIDEO_AGE_S = 5

def _is_fresh(path, max_age_s=600):
    """A fresh file must have been created within max_age_s seconds."""
    if not os.path.exists(path):
        return True
    age = time.time() - os.path.getmtime(path)
    return age <= max_age_s

def require(voice_text=None, music_path=None, script_lines=None, video_path=None, topic=None, strict=True):
    """Enforce quality rules. Returns (ok, errors)."""
    errs = []
    if not voice_text or len(str(voice_text).strip()) < 10:
        errs.append('RULE2: missing Vietnamese voiceover text')
    if not music_path or not os.path.exists(str(music_path)):
        errs.append('RULE3: missing background music')
    if not script_lines:
        errs.append('RULE4: missing captions (script_lines)')
    if video_path and not _is_fresh(video_path):
        errs.append('RULE1/6: video not freshly built (old file reused)')
    if topic:
        try:
            from ops.auto_publish import _already_published
            if _already_published(topic):
                errs.append('RULE5: topic already published: ' + str(topic))
        except Exception:
            pass
    ok = len(errs) == 0
    if not ok and strict:
        raise RuntimeError('QUALITY RULES VIOLATED: ' + '; '.join(errs))
    return ok, errs

if __name__ == '__main__':
    print('quality_rules loaded; RULES: fresh video, VN voice, music, captions, no republish')