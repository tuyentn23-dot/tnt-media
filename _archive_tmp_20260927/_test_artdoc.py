# -- coding: utf-8 --
import os, sys, io, time
sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from ops import art_doc as ad

os.makedirs(ad.ASSETS, exist_ok=True)
img = os.path.join(ad.ASSETS, 'mona_lisa.jpg')
print('img exists:', os.path.exists(img))

# test TTS
mp3 = os.path.join(ad.OUTDIR, '_test_tts.mp3')
print('tts...')
ad.tts_long('Xin chao, day la ban thu nghiem giong doc tieng Viet cho video dai ve hoi hoa.', mp3)
print('mp3 size:', os.path.getsize(mp3) if os.path.exists(mp3) else 0)
dur = ad._ffprobe_dur(mp3)
print('mp3 dur:', round(dur, 2))

# test render segment
seg = os.path.join(ad.OUTDIR, '_test_seg.mp4')
print('render segment...')
ad.render_segment(img, 'Mona Lisa - nu cuoi bi an', mp3, seg, dur + 0.6, 0)
print('seg size:', os.path.getsize(seg) if os.path.exists(seg) else 0)
print('seg dur:', round(ad._ffprobe_dur(seg), 2))
