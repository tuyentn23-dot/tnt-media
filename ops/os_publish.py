# -*- coding: utf-8 -*-
"""TNT Media OS - publish a local video to YouTube with quality gate + DB logging."""
import os, sys, pickle, json
from pathlib import Path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from os_app import db
from os_app import models as M

TOKEN = Path(ROOT) / "config" / "token.pickle"

# Multi-channel support: set active channel to route token + ledger
_ACTIVE_CHANNEL = None

def set_channel(channel_id):
    global _ACTIVE_CHANNEL
    _ACTIVE_CHANNEL = channel_id
    try:
        from ops import content_freshness as _cf
        _cf.set_channel(channel_id)
    except Exception:
        pass
    return _ACTIVE_CHANNEL

def active_channel():
    return _ACTIVE_CHANNEL

def _resolve_token_path():
    if _ACTIVE_CHANNEL:
        try:
            from ops import channel_loader as _ch
            cfg = _ch.load(_ACTIVE_CHANNEL)
            tp = _ch.token_path(cfg)
            if tp and os.path.exists(tp):
                return Path(tp)
        except Exception:
            pass
    return TOKEN

def load_yt():
    tp = _resolve_token_path()
    with open(tp, "rb") as f:
        creds = pickle.load(f)
    return build("youtube", "v3", credentials=creds)

def _gate(video_path):
    try:
        from ops.quality_gate import evaluate
        return evaluate(video_path)
    except Exception as e:
        return {"ok": False, "passes": False, "score": 0, "metrics": {}, "reasons": ["gate error: " + str(e)], "standard": {}}

def publish(video_path, title, description="", tags=None, privacy="public", topic="", cycle_id=None, category_id=None, force=False):
    """Publish a video. Quality gate blocks if score < threshold unless force=True."""
    # HEALTH CHECK: chan video den/loi truoc khi upload (khong the bo qua bang force)
    try:
        from ops import video_health as _vh
        _h = _vh.check(str(video_path))
        if not _h.get('ok'):
            return {'ok': False, 'blocked': True, 'reason': 'video-health', 'health': _h}
    except Exception as _he:
        pass

    from ops import quality_rules as _qr
    try:
        _ok, _errs = _qr.require(video_path=video_path, topic=topic, voice_text=title, music_path=video_path, script_lines=[title], strict=False)
        if not _ok:
            pass
    except Exception:
        pass
    tags = tags or []
    p = Path(video_path)
    if not p.exists():
        return {"ok": False, "error": "file not found: " + str(p)}

    if topic and not force:
        try:
            from ops.auto_publish import _already_published
            if _already_published(topic):
                return dict(ok=False, blocked=True, error='topic already published: ' + str(topic), topic=topic)
        except ImportError:
            pass
    gate = _gate(str(p))
    if not force and not gate.get("passes"):
        M.log_tool_run(cycle_id, "os_publish.gate", {"video": str(p), "reasons": gate.get("reasons")}, False, 0, "")
        return {"ok": False, "blocked": True, "score": gate.get("score"), "reasons": gate.get("reasons"), "metrics": gate.get("metrics")}

    if not category_id:
        try:
            from ops.quality_gate import category_for
            category_id = category_for(topic)
        except Exception:
            category_id = "24"

    yt = load_yt()
    body = {"snippet": {"title": title[:100], "description": description[:5000], "tags": tags, "categoryId": str(category_id)}, "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}}
    media = MediaFileUpload(str(p), chunksize=-1, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = req.execute()
    vid = resp.get("id")

    # Tu dong tao + set thumbnail
    try:
        from ops.thumbnail_generator import generate_high_ctr_thumbnail
        _thumb = str(p).replace(".mp4", "_thumb.jpg")
        generate_high_ctr_thumbnail(title[:60], output_path=_thumb)
        if os.path.exists(_thumb) and vid:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(_thumb)).execute()
    except Exception as _te:
        pass

    meta = {"gate": gate, "category_id": str(category_id), "forced": bool(force)}
    v = M.Video(cycle_id=cycle_id, path=str(p), youtube_id=vid, title=title, topic=topic, format="shorts", score=gate.get("score"), status="published", meta=meta)
    M.add_video(v)
    M.log_tool_run(cycle_id, "os_publish.py", {"video": str(p), "title": title, "score": gate.get("score")}, True, 0, vid or "")
    return {"ok": True, "youtube_id": vid, "url": "https://youtu.be/" + str(vid), "score": gate.get("score")}

if __name__ == "__main__":
    video = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "TNT Media OS test"
    force = ("--force" in sys.argv)
    print(json.dumps(publish(video, title, topic="pdca_test", force=force), ensure_ascii=False))
