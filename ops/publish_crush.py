import os, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
print('active channel:', OP.active_channel())
item = {
	'id': 'gacha_crush',
	'hook': 'Crush của tôi không biết tôi tồn tại',
	'body': 'Mỗi ngày tôi đều nhìn cậu ấy từ xa. Tim tôi đập loạn nhịp nhưng cậu ấy chẳng hề hay biết.',
	'payoff': 'Rồi một ngày, cậu ấy quay lại và hỏi tên tôi. Khoảnh khắc đó tôi không thở nổi.'
}
video = os.path.abspath('output/Mialinhcute_gacha_crush.mp4')
title = item['hook'][:90] + ' #shorts'
desc = item['hook'] + chr(10) + chr(10) + '#gacha #shorts #viral #anime #cute'
tags = ['gacha', 'shorts', 'viral', 'anime', 'cute', 'mia linh cute']
topic = 'chMialinhcute_gacha_crush_' + time.strftime('%Y%m%d_%H%M%S')
print('title:', title)
print('topic:', topic)
r = OP.publish(video, title, description=desc, tags=tags, privacy='public', topic=topic, force=True)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))