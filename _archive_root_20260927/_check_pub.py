import sys,sqlite3
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
sys.path.insert(0,'.')
c=sqlite3.connect('state/pipeline.db')
c.row_factory=sqlite3.Row
rows=c.execute("SELECT channel_id, title, file_path, status, youtube_id FROM publications WHERE channel_id IN ('vilevi5676','Mialinhcute') ORDER BY id DESC LIMIT 20").fetchall()
for r in rows:
 print(dict(r))
