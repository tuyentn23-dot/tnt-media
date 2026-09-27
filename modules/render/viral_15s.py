# -*- coding: utf-8 -*-
"""Safe module-only renderer for an exact 15-second viral follow-up preview."""
import os
import subprocess
import tempfile

MODULE = {
    "name": "render.viral_15s",
    "version": "1.0.2",
    "interface": "render(item: dict, out: str, style: dict = None) -> str",
    "config_schema": {"item": "dict", "out": "str", "style": "dict"},
    "deps": ["render.video"],
    "health": "True",
}


def render(item, out, style=None):
    from modules.render import video as base
    from ops.ffmpeg_render import FFMPEG

    target = float(item.get("duration_seconds") or 15.0)
    if abs(target - 15.0) > 0.001:
        raise ValueError("viral_15s requires duration_seconds=15")

    out_abs = os.path.abspath(out)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="viral15_", suffix=".mp4", dir=os.path.dirname(out_abs))
    os.close(fd)
    try:
        if os.path.exists(tmp):
            os.remove(tmp)
        import ops.ffmpeg_render as fr
        original_pool = fr._fresh_or_pool
        def local_pool(local_item, seed):
            return fr.pickpool(local_item.get("topic", ""), seed)
        fr._fresh_or_pool = local_pool
        try:
            base.render(item, tmp, style=style or {})
        finally:
            fr._fresh_or_pool = original_pool
        if not os.path.exists(tmp) or os.path.getsize(tmp) < 300000:
            raise RuntimeError("base render output missing or too small")

        cmd = [
            FFMPEG, "-y", "-stream_loop", "-1", "-i", tmp,
            "-t", "15", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "21", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-shortest", out_abs,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out_abs) or os.path.getsize(out_abs) < 300000:
            raise RuntimeError("15s normalization failed: " + (r.stderr or "")[-500:])
        return out_abs
    finally:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass


def health():
    try:
        from modules.render import video
        from ops.ffmpeg_render import FFMPEG
        return bool(video.health() and FFMPEG and os.path.exists(FFMPEG))
    except Exception:
        return False
