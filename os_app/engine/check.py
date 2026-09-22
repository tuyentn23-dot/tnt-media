"""TNT Media OS - CHECK stage."""
from .. import models as M
from ..adapters import youtube_metrics as YT

def _quality_audit(cycle_id, limit=5):
    """Score published videos that lack a score; emit insights."""
    try:
        from ops.quality_gate import evaluate
    except Exception as e:
        return []
    out = []
    try:
        vids = M.list_videos(limit=50)
    except Exception:
        return []
    n = 0
    for v in vids:
        if n >= limit:
            break
        if v.get("score") is not None:
            continue
        path = v.get("path")
        if not path or not __import__("os").path.exists(path):
            continue
        res = evaluate(path)
        sc = res.get("score", 0)
        try:
            M.update_video(v.get("id"), score=sc)
        except Exception:
            pass
        finding = "Video score " + str(sc) + " passes=" + str(res.get("passes"))
        M.add_insight(M.Insight(cycle_id=cycle_id, kind="quality_audit", finding=finding, evidence=res))
        out.append(finding)
        n += 1
    return out

def run(cycle_id, limit=20):
    insights = []
    ch = YT.fetch_channel_stats()
    if ch and "views" in ch:
        finding = "Channel " + ch.get("title", "?") + ": " + str(ch["views"]) + " views, " + str(ch["subs"]) + " subs, " + str(ch["videos"]) + " videos"
        M.add_insight(M.Insight(cycle_id=cycle_id, kind="channel_snapshot", finding=finding, evidence=ch))
        insights.append(finding)
    res = YT.ingest_all_published(limit=limit)
    for rec in res:
        r = rec.get("result") or {}
        data = r.get("data", {}) if isinstance(r, dict) else {}
        views = data.get("views", 0)
        if views >= 1:
            finding = "Video " + str(rec["youtube_id"]) + " reached " + str(views) + " views"
            M.add_insight(M.Insight(cycle_id=cycle_id, kind="top_performer", finding=finding, evidence=data))
            insights.append(finding)
    q = _quality_audit(cycle_id, limit=5)
    insights.extend(q)
    return {"ingested": len(res), "insights": insights, "quality": q}
