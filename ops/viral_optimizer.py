# Viral Optimizer - TNT Media (2026-09-11)
# Enforces ALL viral levers: no-voice top topics, perfect loop, hook, 13-20s, music bed, viral gate.
import os
import json
import logging
from datetime import datetime
from ops.compat import get_video_clip, get_audio_clip, subclip

logging.basicConfig(filename="output/viral_manager.log", level=logging.INFO)
log = logging.getLogger("viral")
SWEET_MIN = 13
SWEET_MAX = 20
NO_VOICE_TOPICS = ["satisfying", "food", "magic"]

def score_video(path):
    info = {"path": path}
    score = 0
    try:
        V = get_video_clip()
        c = V(path)
        dur = c.duration
        info["duration"] = round(dur, 2)
        inrange = SWEET_MIN <= dur <= SWEET_MAX
        score = score + 40 if inrange else score
        info["sweet_spot"] = inrange
        hasaudio = c.audio is not None
        score = score + 20 if hasaudio else score
        info["has_audio"] = hasaudio
        vert = bool(c.h and c.w and c.h > c.w)
        score = score + 20 if vert else score
        info["vertical"] = vert
        short = dur > 0 and dur <= 60
        score = score + 20 if short else score
        c.close()
    except Exception as e:
        info["error"] = str(e)
    info["viral_score"] = score
    return info

def gate(path, min_score=80):
    info = score_video(path)
    info["passes_gate"] = info.get("viral_score", 0) >= min_score
    return info

def apply_music(video_path, music_path, output_path):
    try:
        V = get_video_clip()
        A = get_audio_clip()
        clip = V(video_path)
        music = A(music_path)
        from moviepy.audio.AudioClip import concatenate_audioclips
        reps = int(clip.duration / max(0.1, music.duration)) + 1
        music = concatenate_audioclips([music] * reps)
        music = music.subclipped(0, clip.duration)
        music = music.with_volume_scaled(0.3)
        final = clip.with_audio(music)
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        return output_path
    except Exception as e:
        log.warning("music apply failed: " + str(e))
        return None

def optimize_viral(input_path, output_path=None, target=15, music_path=None):
    from ops.retention_optimizer import optimize as retention
    if output_path is None:
        output_path = input_path.replace(".mp4", "_viral.mp4")
    mid = output_path.replace(".mp4", "_mid.mp4")
    retention(input_path, output_path=mid, target=target)
    if music_path and os.path.exists(music_path):
        res = apply_music(mid, music_path, output_path)
        return output_path if res else mid
    import shutil
    shutil.copyfile(mid, output_path)
    return output_path
