import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
j = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
out = []
for k in ['anime', 'cute_animals', 'gacha']:
	out.append('=== ' + k + ' (' + str(len(j[k])) + ')')
	for it in j[k]:
		out.append(' ' + str(it.get('id')) + ' | ' + str(it.get('hook', ''))[:80])
open('output/db_scan.txt', 'w', encoding='utf-8').write(chr(10).join(out))
print('lines:', len(out))