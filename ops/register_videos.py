# -- coding: utf-8 --
# Dang ky 8 video moi thanh publications
import os, sys, io, json
sys.path.insert(0, '.')
from pipeline import state

VIDEOS = [
	('Mialinhcute', 'gacha', 'gacha_new_01', 'Cô gái Gacha bỏ học vì gia đình nghèo'),
	('Mialinhcute', 'anime', 'anime_new_01', 'Naruto mạnh nhất khi nào?'),
	('Mialinhcute', 'cute_animals', 'cute_new_01', 'Mèo con lần đầu nhìn thấy tuyết'),
	('Mialinhcute', 'meme', 'meme_new_01', 'Khi mẹ gọi dậy đi học lúc 5 giờ sáng'),
	('vilevi5676', 'whatif', 'whatif_new_01', 'Điều gì xảy ra nếu Mặt Trời đột ngột tắt?'),
	('vilevi5676', 'facts', 'facts_new_01', 'Vì sao bầu trời có màu xanh?'),
	('vilevi5676', 'curiosity', 'curio_new_01', 'Cá heo có thể nhận ra mình trong gương không?'),
	('vilevi5676', 'food', 'food_new_01', 'Phở Việt Nam có nguồn gốc từ đâu?'),
]

outdir = 'output'
c = state.init()
found = {}
for f in os.listdir(outdir):
	if f.endswith('.mp4') and 'new' in f:
		for cid, kind, iid, title in VIDEOS:
			if cid in f and iid in f:
				found[(cid, iid)] = os.path.join(outdir, f)

print('found', len(found), 'videos')
for (cid, iid), path in found.items():
	title = [t for c,k,i,t in VIDEOS if i==iid][0]
	sig = 'pub_' + cid + '_' + iid
	try:
		c.execute('INSERT OR IGNORE INTO publications (job_id, channel_id, signature, topic, kind, title, file_path, status, created_at) VALUES (?,?,?,?,?,?,?,?,?)',
			('manual', cid, sig, kind, kind, title, path, 'rendered', state.now()))
		c.commit()
		print('registered', cid, iid)
	except Exception as e:
		print('ERR', iid, str(e)[:80])
print('done')
