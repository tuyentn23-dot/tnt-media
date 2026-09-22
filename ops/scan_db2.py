import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
for k in ['anime', 'cute_animals', 'gacha']:
	print('===', k)
	for it in d[k]:
		print(' ', it.get('id'), '|', str(it.get('hook', ''))[:80])