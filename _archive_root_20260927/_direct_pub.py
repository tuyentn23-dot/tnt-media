# -- coding: utf-8 --
import os, sys, importlib, time
sys.path.insert(0, os.getcwd())
op = importlib.import_module('ops.os_publish')
op_set = getattr(op, 'set_channel')
op_pub = getattr(op, 'publish')
ITEMS = [
	('output/chMialinhcute_anime_anime_dragonball_20260924_191802.mp4', 'Mialinhcute', 'Goku manh den muc nao?'),
	('output/chMialinhcute_roblox_roblox_mm2_20260924_192352.mp4', 'Mialinhcute', 'Dao huyen thoai trong MM2 o dau ra?'),
	('output/chMialinhcute_cute_animals_animal_axolotl_20260924_193030.mp4', 'Mialinhcute', 'Axolotl co the tai sinh nao khong?'),
	('output/chvilevi5676_life_morning_1_20260924_161350.mp4', 'vilevi5676', 'Buoi sang som cua Sai Gon'),
]
def run():
	for path, channel, title in ITEMS:
		if not os.path.exists(path):
			print('MISSING:', path)
			continue
		base = os.path.basename(path).replace('.mp4', '')
		topic = base + '_' + time.strftime('%Y%m%d_%H%M%S')
		print()
		print('===', channel, topic)
		op_set(channel)
		try:
			res = op_pub(path, title, description='', tags=None, privacy='public', topic=topic)
			print('RESULT:', res)
		except Exception as e:
			print('ERR:', str(e)[:300])
if __name__ == '__main__':
	run()
