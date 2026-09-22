import sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
g = d['gacha']
for i, it in enumerate(g):
	print(i, it.get('id', '?'), '|', str(it.get('hook', ''))[:70])