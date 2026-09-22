import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import channel_producer as CP
# lay item gacha dau tien chua dang
items = CP.load_items('Mialinhcute')
pubd = CP.published_titles()
gacha_items = [(k, it) for k, it in items if k == 'gacha']
print('total gacha:', len(gacha_items))
fresh = []
for k, it in gacha_items:
	hook = it.get('hook', '').strip().rstrip('.') + ' #shorts'
	if hook not in pubd:
		fresh.append((k, it))
print('fresh gacha:', len(fresh))
for k, it in fresh:
	print(' -', it.get('id'), '|', it.get('hook', '')[:60])