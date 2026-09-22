"""TNT Media OS - migrate legacy JSON (published.json + analytics) into SQLite."""
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(os.getcwd())))
from os_app import db
from os_app import models as M

HERE = Path(os.getcwd())
PUB = HERE / "memory" / "published.json"

def migrate_published():
    if not PUB.exists():
        return 0
    data = json.loads(PUB.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        data = data.get("videos", [])
    n = 0
    for rec in data:
        vid = rec.get("video_id")
        is_mock = bool(vid and "MOCK" in str(vid))
        v = M.Video(title=rec.get("title"), topic=rec.get("topic"), score=rec.get("score"), youtube_id=(None if is_mock else vid), status="published", meta={"source": "legacy", "mock": is_mock})
        M.add_video(v)
        n += 1
    return n

def run():
    db.init()
    n = migrate_published()
    print("migrated " + str(n) + " records")
    return n

if __name__ == "__main__":
    run()

