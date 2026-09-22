"""TNT Media OS - YouTube metrics ingestion."""
import json
import os
from pathlib import Path
from .. import db
from .. import models as M

HERE = Path(os.getcwd())
TOKEN = HERE / "memory" / "token.json"

def _build():
    if not TOKEN.exists():
        return None
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    c = Credentials.from_authorized_user_file(str(TOKEN))
    return build("youtube", "v3", credentials=c)

def fetch_stats(video_id):
    yt = _build()
    if not yt:
        return None
    try:
        r = yt.videos().list(part="statistics,snippet", id=video_id).execute()
        items = r.get("items", [])
        if not items:
            return None
        s = items[0].get("statistics", {})
        return {"views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)), "comments": int(s.get("commentCount", 0))}
    except Exception as e:
        return {"error": str(e)}

def ingest_for_video(video_db_id, youtube_id):
    st = fetch_stats(youtube_id)
    if not st:
        return None
    if "error" in st:
        return st
    m = M.Metric(video_id=video_db_id, views=st.get("views", 0), likes=st.get("likes", 0), comments=st.get("comments", 0), source="youtube", raw=st)
    mid = M.add_metric(m)
    return {"metric_id": mid, "data": st}

def ingest_all_published(limit=20):
    vids = [v for v in M.list_videos(limit) if v.get("youtube_id")]
    out = []
    for v in vids[:limit]:
        r = ingest_for_video(v["id"], v["youtube_id"])
        out.append({"video_id": v["id"], "youtube_id": v["youtube_id"], "result": r})
    return out

def fetch_channel_stats():
    yt = _build()
    if not yt:
        return None
    try:
        r = yt.channels().list(part="statistics,snippet,contentDetails", mine=True).execute()
        items = r.get("items", [])
        if not items:
            return None
        it = items[0]
        s = it.get("statistics", {})
        return {"title": it["snippet"]["title"], "views": int(s.get("viewCount", 0)), "subs": int(s.get("subscriberCount", 0)), "videos": int(s.get("videoCount", 0))}
    except Exception as e:
        return {"error": str(e)}

