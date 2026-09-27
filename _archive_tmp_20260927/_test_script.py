# -- coding: utf-8 --
import os, sys, io, json, time
sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from ops import art_doc as ad

facts = ('Mona Lisa cua Leonardo da Vinci, ve khoang 1503-1519, hien o bao tang Louvre Paris. '
	'Nu cuoi bi an, anh mat nhu doi theo nguoi xem. Bi danh La Gioconda.')
t = time.time()
sc = ad.write_script('Mona Lisa', facts, sections=3)
dt = round(time.time() - t, 1)
print('LLM time:', dt)
print('title:', (sc or {}).get('title'))
parts = (sc or {}).get('parts', [])
print('parts:', len(parts))
for p in parts:
	print('---', p.get('heading'))
	print((p.get('text') or '')[:200])
open('projects/art_doc/_test_script.json', 'w', encoding='utf-8').write(json.dumps(sc, ensure_ascii=False, indent=2))
