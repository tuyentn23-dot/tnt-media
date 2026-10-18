# coding utf8
"""Re-verify PUBLISHED videos periodically to catch post-publish takedowns.

Existing verify_pubs only checks yt_verified_at IS NULL, so a video taken
down AFTER its first verify never gets caught. This script re-checks
published rows whose last yt_verified_at is older than --max-age-hours.
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))

from pipeline import state
from pipeline.verify_pubs import _yt


def reverify(max_age_hours=24, limit=200, dry_run=False):
	cutoff = (datetime.now() - timedelta(hours=max_age_hours)).isoformat(timespec="seconds")
	c = state.connect()
	rows = c.execute(
		"SELECT id, channel_id, youtube_id, yt_verified_at FROM publications "
		"WHERE status='published' AND youtube_id IS NOT NULL AND youtube_id != '' "
		"AND (yt_verified_at IS NULL OR yt_verified_at < ?) LIMIT ?",
		(cutoff, limit),
	).fetchall()
	res = {"checked": 0, "alive": 0, "dead": 0, "flagged": 0, "dry_run": bool(dry_run), "details": []}
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
			if not dry_run:
				c.execute(
					"UPDATE publications SET yt_verified_at=?, yt_verify_attempts=yt_verify_attempts+1 WHERE id=?",
					(state.now(), r["id"]),
				)
		else:
			res["dead"] += 1
			if not dry_run:
				# For reverify: dead after a prior successful verify = takedown -> flag immediately.
				c.execute(
					"UPDATE publications SET yt_verify_attempts=yt_verify_attempts+1, status='verify_failed' WHERE id=?",
					(r["id"],),
				)
				res["flagged"] += 1
		res["details"].append(
			{"id": r["id"], "channel": ch, "youtube_id": yid, "alive": alive, "reason": reason}
		)
	if not dry_run:
		c.commit()
	return res


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("--max-age-hours", type=float, default=24)
	ap.add_argument("--limit", type=int, default=200)
	ap.add_argument("--dry-run", action="store_true")
	a = ap.parse_args()
	print(json.dumps(reverify(a.max_age_hours, a.limit, a.dry_run), ensure_ascii=False, indent=2))
