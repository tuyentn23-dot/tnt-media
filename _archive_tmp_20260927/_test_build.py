# -- coding: utf-8 --
import os, sys, io, json, time
sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from ops import art_doc as ad

img = os.path.join(ad.ASSETS, 'mona_lisa.jpg')
images = [img]

# fake script (3 short parts) to test full render path
fake = {'title': 'Test', 'hook': 'hook', 'parts': [
	{'heading': 'Phần 1', 'text': 'Mona Lisa là bức tranh nổi tiếng nhất thế giới. Nàng cười bí ẩn.'},
	{'heading': 'Phần 2', 'text': 'Bức tranh được vẽ bởi Leonardo da Vinci trong nhiều năm.'},
	{'heading': 'Phần 3', 'text': 'Ngày nay nó nằm trong bảo tàng Louvre ở Paris.'},
]}

# monkeypatch write_script to use fake
ad.write_script = lambda art, facts, sections=8: fake

t = time.time()
final, sc = ad.build_art_video('Test', 'facts', images, 'testrun', sections=3)
print('BUILD TIME', round(time.time()-t,1))
print('FINAL:', final, os.path.getsize(final) if os.path.exists(final) else 0)
print('DUR:', round(ad._ffprobe_dur(final),1))
