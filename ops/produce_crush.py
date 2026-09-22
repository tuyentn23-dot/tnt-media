import os, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import channel_producer as CP
items = CP.load_items('Mialinhcute')
item = None
for k, it in items:
	if it.get('id') == 'gacha_crush':
		item = it
		break
print('item:', item.get('id'))
print('hook:', item.get('hook'))
# render (khong publish)
r = CP.produce('Mialinhcute', 'gacha', item, live=False)
print(json.dumps(r, ensure_ascii=False, indent=2))