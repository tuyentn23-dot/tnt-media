# coding utf8
"""Verify published YouTube videos actually exist; record yt_verified_at."""
import json
import urllib.request
import urllib.error
from datetime import datetime

from os_app import db


def _now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def check_video(video_id, timeout=10):
    """Return (alive: bool, reason: str). Uses oEmbed (no quota)."""
    url = "https://www.youtube.com/oembed?url=https://youtu.be/" + video_id + "&format=json"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            if r.status == 200:
                return True, "ok"
            return False, "http" + str(r.status)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "not_found"
        if e.code == 401:
            return False, "private"
        return False, "http_" + str(e.code)
    except Exception as e:
        return False, "network_" + type(e).__name__


def verify_pending(limit=50):
    results = {"checked": 0, "alive": 0, "dead": 0, "details": []}
    with db.tx() as c:
        rows = c.execute(
            "SELECT id, youtube_id FROM videos WHERE status='published' AND youtube_id IS NOT NULL AND youtube_id != '' AND yt_verified_at IS NULL LIMIT ?",
            (limit,),
        ).fetchall()
    for row in rows:
        vid_id = row["id"]
        yt = row["youtube_id"]
        alive, reason = check_video(yt)
        results["checked"] += 1
        if alive:
            results["alive"] += 1
            with db.tx() as c:
                c.execute(
                    "UPDATE videos SET yt_verified_at=?, yt_verify_attempts=yt_verify_attempts+1 WHERE id=?",
                    (_now(), vid_id),
                )
        else:
            results["dead"] += 1
            with db.tx() as c:
                c.execute(
                    "UPDATE videos SET yt_verify_attempts=yt_verify_attempts+1, status=CASE WHEN yt_verify_attempts>=2 THEN 'failed_verify' ELSE status END WHERE id=?",
                    (vid_id,),
                )
        results["details"].append({"id": vid_id, "youtube_id": yt, "alive": alive, "reason": reason})
    return results


if __name__ == "__main__":
    print(json.dumps(verify_pending(), ensure_ascii=False, indent=2))
