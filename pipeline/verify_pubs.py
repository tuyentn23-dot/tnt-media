# coding utf8
"""Verify published YouTube videos against their own channel token."""
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))

from pipeline import state


def _yt(channel_id):
	import pickle
	from googleapiclient.discovery import build
	tp = ROOT / "channels" / channel_id / "token.pickle"
	if not tp.exists():
		return None, "no_token"
	try:
		creds = pickle.load(open(tp, "rb"))
		return build("youtube", "v3", credentials=creds), None
	except Exception as e:
		return None, "token_err:" + type(e).__name__


def verify_pending(limit=100):
	c = state.connect()
	rows = c.execute(
		"SELECT id, channel_id, youtube_id FROM publications "
		"WHERE status='published' AND youtube_id IS NOT NULL AND youtube_id != '' "
		"AND yt_verified_at IS NULL LIMIT ?",
		(limit,),
	).fetchall()
	res = {"checked": 0, "alive": 0, "dead": 0, "details": []}
	cache = {}
	for r in rows:
		res["checked"] += 1
		ch = r["channel_id"]
		yid = r["youtube_id"]
		if ch not in cache:
			cache[ch] = _yt(ch)[0]
		yt = cache[ch]
		alive = False
		reason = "no_api"
		if yt is not None:
			try:
				resp = yt.videos().list(part="id,status", id=yid).execute()
				items = resp.get("items", [])
				if items:
					alive = True
					reason = items[0].get("status", {}).get("privacyStatus", "ok")
				else:
					reason = "not_found"
			except Exception as e:
				reason = "err:" + type(e).__name__
		if alive:
			res["alive"] += 1
			c.execute("UPDATE publications SET yt_verified_at=?, yt_verify_attempts=yt_verify_attempts+1 WHERE id=?", (state.now(), r["id"]))
		else:
			res["dead"] += 1
			c.execute("UPDATE publications SET yt_verify_attempts=yt_verify_attempts+1, status=CASE WHEN yt_verify_attempts>=2 THEN 'verify_failed' ELSE status END WHERE id=?", (r["id"],))
		res["details"].append({"id": r["id"], "channel": ch, "youtube_id": yid, "alive": alive, "reason": reason})
	c.commit()
	return res


if __name__ == "__main__":
	print(json.dumps(verify_pending(), ensure_ascii=False, indent=2))
