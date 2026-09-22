# -- coding: utf-8 --
import os, sys, io
sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from ops import art_doc as ad
t = ' '.join(['Đây là câu thử nghiệm số ' + str(i) + ' về bức tranh nổi tiếng.' for i in range(40)])
ad.tts_long(t, 'output/_tts_long.mp3')
print('size', os.path.getsize('output/_tts_long.mp3'))
