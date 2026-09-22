import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import voice_synth as VS
# 1. Tao voice tu text
text = 'Crush của tôi không biết tôi tồn tại. Tôi thầm thương cậu ấy suốt hai năm. Rồi một ngày, cậu ấy quay lại và mỉm cười với tôi.'
vo = os.path.abspath('output/ai_vo_crush.mp3')
VS.synth_parts([text], vo, voice='female_north', preset='cute', gap=0.4)
print('voice:', os.path.getsize(vo))