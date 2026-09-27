import sys, json, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from ops import channel_loader as ch
items = ch.load_content('Mialinhcute', 'gacha')
print('count:', len(items))
if items:
	print(json.dumps(items[0], ensure_ascii=False, indent=2)[:1500])
