import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import voice_synth as VS
parts = [
	'Pikachu có thực sự là chuột? Đây là bí mật ít ai biết!',
	'Pikachu được tạo hình dựa trên loài sóc chuột Nhật Bản, không phải chuột thường!',
	'Đôi má đỏ của Pikachu có thể tích điện tới hàng nghìn volt!',
	'Và đây là sự thật thú vị: Pikachu là linh vật có sức ảnh hưởng nhất mọi thời đại!'
]
vo = os.path.abspath('output/pika_vo.mp3')
VS.synth_parts(parts, vo, voice='female_north', preset='cute', gap=0.35)
print('voice:', os.path.getsize(vo))