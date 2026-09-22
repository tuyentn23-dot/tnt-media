import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
for k, v in d.items():
	print('===', k, len(v))
	for it in v[:10]:
		print(' ', it.get('id'), '|', str(it.get('hook', ''))[:70])