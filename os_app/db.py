import os
import sqlite3
import threading
import json
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).resolve()
DB_PATH = ROOT / "memory" / "tnt_media.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
SCHEMA_FILE = ROOT / "os_app" / "schema.sql"
LOCK = threading.Lock()

def now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def connect():
    c = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    return c

@contextmanager
def tx():
    with LOCK:
        c = connect()
        try:
            yield c
            c.commit()
        except Exception:
            c.rollback()
            raise
        finally:
            c.close()

def init():
    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    with tx() as c:
        c.executescript(sql)
    _migrate()

# Columns added after initial release; safe additive migration.
_MIGRATIONS = {
    "videos": {
        "yt_verified_at": "TEXT",
        "yt_verify_attempts": "INTEGER NOT NULL DEFAULT 0",
    },
}

def _migrate():
    with tx() as c:
        for table, cols in _MIGRATIONS.items():
            cur = c.execute("PRAGMA table_info(%s)" % table)
            existing = {r[1] for r in cur.fetchall()}
            for col, decl in cols.items():
                if col not in existing:
                    c.execute("ALTER TABLE %s ADD COLUMN %s %s" % (table, col, decl))

TABLES = ["cycles","videos","metrics","insights","decisions","experiments","tool_runs"]

def health():
    with tx() as c:
        counts = {}
        for t in TABLES:
            qry = "SELECT COUNT(*) n FROM " + t
            counts[t] = c.execute(qry).fetchone()["n"]
    return {"db": str(DB_PATH), "counts": counts}

if __name__ == "__main__":
 init()
 print(json.dumps(health(), indent=2))
