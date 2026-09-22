import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
from os_app import db
OP.set_channel('Mialinhcute')
yt = OP.load_yt()
c = db.connect()
rows = c.execute('SELECT youtube_id, title, topic FROM videos WHERE youtube_id IS NOT NULL ORDER BY rowid DESC LIMIT 60').fetchall()
ids = [r[0] for r in rows]
info = {}
for i in range(0, len(ids), 50):
	r = yt.videos().list(part='statistics', id=','.join(ids[i:i+50])).execute()
	for it in r.get('items', []):
		info[it['id']] = it.get('statistics', {})
out = [{'title': r[1], 'topic': r[2], 'views': int(info.get(r[0], {}).get('viewCount', 0)), 'likes': int(info.get(r[0], {}).get('likeCount', 0))} for r in rows]
json.dump(out, open('memory/metrics_snapshot.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('SNAPSHOT SAVED', len(out))
