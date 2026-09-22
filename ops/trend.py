import os, json, glob
from datetime import datetime, date, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")
HIST = os.path.join(MEM, "history")
REG = os.path.join(MEM, "channels.json")
CHAN = os.path.join(MEM, "channel_real.json")
PERF = os.path.join(MEM, "performance.json")

def _load(p, d=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return d

def _write(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + ".tmp"
    json.dump(o, open(t, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(t, p)

def channels():
    reg = _load(REG, {})
    lst = reg.get("channels", []) if isinstance(reg, dict) else []
    if not lst:
        ch = _load(CHAN, {})
        if ch:
            lst = [{"id": ch.get("id"), "title": ch.get("title"), "active": True}]
    return lst

def active_channel_id():
    reg = _load(REG, {})
    if isinstance(reg, dict) and reg.get("active"):
        return reg["active"]
    c = channels()
    return c[0]["id"] if c else None

def snapshot(cid=None, force=False):
    cid = cid or active_channel_id()
    ch = _load(CHAN, None)
    if not ch or "subs" not in ch:
        return {"ok": False, "reason": "no channel data"}
    today = date.today().isoformat()
    path = os.path.join(HIST, (cid or "default") + "_" + today + ".json")
    if os.path.exists(path) and not force:
        return {"ok": True, "written": False, "date": today}
    s = {"ts": datetime.now().isoformat(timespec="seconds"), "date": today, "id": cid,
        "title": ch.get("title"), "subs": int(ch.get("subs", 0)),
        "views": int(ch.get("views", 0)), "videos": int(ch.get("videos", 0))}
    _write(path, s)
    return {"ok": True, "written": True, "date": today}

def _series(cid=None):
    cid = cid or active_channel_id() or "default"
    out = []
    for p in sorted(glob.glob(os.path.join(HIST, cid + "*.json"))):
        d = _load(p, None)
        if d and "date" in d and "subs" in d:
            out.append(d)
    out.sort(key=lambda x: x["date"])
    return out

def _delta(series, days):
    if len(series) < 2:
        return {"subs": 0, "views": 0, "videos": 0, "days": 0}
    last = series[-1]
    cut = date.fromisoformat(last["date"]) - timedelta(days=days)
    tgt = series[0]
    for s in series[:-1]:
        if date.fromisoformat(s["date"]) <= cut:
            tgt = s
    rd = (date.fromisoformat(last["date"]) - date.fromisoformat(tgt["date"])).days or 1
    return {"subs": int(last.get("subs", 0)) - int(tgt.get("subs", 0)),
            "views": int(last.get("views", 0)) - int(tgt.get("views", 0)),
            "videos": int(last.get("videos", 0)) - int(tgt.get("videos", 0)),
            "days": rd}

def trend(cid=None):
    s = _series(cid)
    cur = _load(CHAN, {})
    d1 = _delta(s, 1)
    d7 = _delta(s, 7)
    d30 = _delta(s, 30)
    cur_d = {"subs": int(cur.get("subs", 0)), "views": int(cur.get("views", 0)), "videos": int(cur.get("videos", 0))}
    vel = {"subs_per_day": round(d7["subs"] / d7["days"], 2) if d7["days"] else 0, "views_per_day": round(d7["views"] / d7["days"], 1) if d7["days"] else 0}
    ser = [{"date": x["date"], "subs": x["subs"], "views": x["views"], "videos": x.get("videos", 0)} for x in s[-30:]]
    return {"current": cur_d, "delta": {"d1": d1, "d7": d7, "d30": d30}, "velocity": vel, "series": ser, "snapshots": len(s)}

def _dedupe():
    perf = _load(PERF, [])
    best = {}
    for v in perf:
        vid = v.get("id")
        if not vid:
            continue
        c = best.get(vid)
        if c is None or int(v.get("views", 0)) > int(c.get("views", 0)):
            best[vid] = v
    return best, len(perf)

def top(limit=5):
    best, raw = _dedupe()
    rows = sorted(best.values(), key=lambda v: int(v.get("views", 0)), reverse=True)
    out = []
    for i, v in enumerate(rows[:limit], 1):
        out.append({"rank": i, "id": v.get("id"), "views": int(v.get("views", 0)),
                "likes": int(v.get("likes", 0)), "comments": int(v.get("comments", 0)),
                "status": v.get("status", "")})
    return {"top": out, "tracked": len(best), "raw_records": raw, "duplicates_removed": raw - len(best)}

def analytics_deduped():
    best, raw = _dedupe()
    return {"views": sum(int(v.get("views", 0)) for v in best.values()),
            "likes": sum(int(v.get("likes", 0)) for v in best.values()),
            "comments": sum(int(v.get("comments", 0)) for v in best.values()),
            "tracked": len(best), "duplicates_removed": raw - len(best)}

def brief(cid=None):
    tr = trend(cid)
    tp = top(5)
    w = []
    if tr["snapshots"] < 2:
        w.append("Chưa đủ dữ liệu lịch sử — mở dashboard vài ngày để thấy xu hướng.")
    d1 = tr["delta"]["d1"]
    if tr["snapshots"] >= 2 and d1["subs"] <= 0 and d1["views"] <= 0:
        w.append("Kênh đứng yên hôm nay — cân nhắc đăng nội dung mới.")
    if tp["duplicates_removed"] > 0:
        w.append("Đã loại %d bản ghi trùng trong performance.json." % tp["duplicates_removed"] )
    return {"generated": datetime.now().isoformat(timespec="seconds"),
        "channel": _load(CHAN, {}).get("title", "?"),
        "delta": tr["delta"], "velocity": tr["velocity"],
        "top": tp["top"], "snapshots": tr["snapshots"], "warnings": w}
