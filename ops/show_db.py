import sqlite3, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
db_path = None
for p in ["memory/tnt.db", "os_app/tnt.db", "tnt.db"]:
 if os.path.exists(p):
 db_path = p
 break
print("db:", db_path)
if db_path:
 c = sqlite3.connect(db_path)
 rows = c.execute("SELECT title, youtube_id FROM videos WHERE youtube_id IS NOT NULL ORDER BY id DESC LIMIT 8").fetchall()
 for t, y in rows:
 print(y, "| ", t[:60])