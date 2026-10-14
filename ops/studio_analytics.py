# ops/studio_analytics.py - YouTube Analytics + Comments cho advisor
import os, sys, pickle, json, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def _creds(channel_id=None):
	if not channel_id:
		channel_id = "ViLe-facts"
	tp = os.path.join(ROOT, "channels", channel_id, "token.pickle")
	if not os.path.exists(tp):
		from ops import studio_advisor as sa
		tp2 = sa._token_path(channel_id)
		tp = tp2 if tp2 else tp
	if not tp or not os.path.exists(tp):
		return None
	return pickle.load(open(tp, "rb"))

def _ch_metrics(ya, base):
	m = ya.reports().query(metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost", **base).execute()
	if not m.get("rows"):
		return {}
	hdr = [h["name"] for h in m["columnHeaders"]]
	return dict(zip(hdr, m["rows"][0]))

def _traffic(ya, base):
	try:
		m = ya.reports().query(metrics="views", dimensions="insightTrafficSourceType", sort="-views", maxResults=10, **base).execute()
		return [{"source": r[0], "views": r[1]} for r in m.get("rows", [])]
	except Exception:
		return []

def _top_videos(ya, base):
	try:
		m = ya.reports().query(metrics="views,estimatedMinutesWatched,averageViewPercentage", dimensions="video", sort="-estimatedMinutesWatched", maxResults=10, **base).execute()
		return [{"video": r[0], "views": r[1], "minutes": r[2], "avg_pct": round(min(float(r[3]), 100.0), 1)} for r in m.get("rows", [])]
	except Exception:
		return []

def fetch_analytics(channel_id=None, days=90):
	try:
		creds = _creds(channel_id)
		if not creds:
			return {"ok": False, "error": "no token"}
		from googleapiclient.discovery import build
		from datetime import date, timedelta
		ya = build("youtubeAnalytics", "v2", credentials=creds)
		end = date.today().isoformat()
		start = (date.today() - timedelta(days=int(days))).isoformat()
		base = {"ids": "channel==MINE", "startDate": start, "endDate": end}
		return {"ok": True, "window_days": int(days), "channel": _ch_metrics(ya, base), "traffic": _traffic(ya, base), "top_by_watchtime": _top_videos(ya, base)}
	except Exception as e:
		return {"ok": False, "error": str(e)[:300]}

def _collect_vids(yt):
	ch = yt.channels().list(part="contentDetails", mine=True).execute()
	items = ch.get("items", [])
	if not items:
		return []
	uploads = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
	pl = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=20).execute()
	return [x["contentDetails"]["videoId"] for x in pl.get("items", [])]

def _vid_comments(yt, vid):
	try:
		cr = yt.commentThreads().list(part="snippet", videoId=vid, maxResults=20, textFormat="plainText", order="relevance").execute()
	except Exception:
		return []
	out = []
	for it in cr.get("items", []):
		sn = it["snippet"]["topLevelComment"]["snippet"]
		out.append({"video": vid, "text": sn.get("textDisplay", "")[:200], "likes": int(sn.get("likeCount", 0)), "at": sn.get("publishedAt", "")[:10]})
	return out

def fetch_comments(channel_id=None, limit=100):
	try:
		creds = _creds(channel_id)
		if not creds:
			return {"ok": False, "error": "no token"}
		from googleapiclient.discovery import build
		yt = build("youtube", "v3", credentials=creds)
		vids = _collect_vids(yt)
		out = []
		for vid in vids[:10]:
			out.extend(_vid_comments(yt, vid))
			if len(out) >= int(limit):
				break
		out.sort(key=lambda x: x["likes"], reverse=True)
		return {"ok": True, "count": len(out), "top": out[:30]}
	except Exception as e:
		return {"ok": False, "error": str(e)[:300]}

if __name__ == "__main__":
	a = fetch_analytics()
	print("ANALYTICS ok=", a.get("ok"), "err=", a.get("error", ""))
	if a.get("ok"):
		print("channel: ", json.dumps(a.get("channel"), ensure_ascii=False))
		print("traffic: ", json.dumps(a.get("traffic")[:5], ensure_ascii=False))
		print("top_videos: ", len(a.get("top_by_watchtime", [])))
	c = fetch_comments(limit=30)
	print("COMMENTS ok=", c.get("ok"), "err=", c.get("error", ""), "count=", c.get("count"))