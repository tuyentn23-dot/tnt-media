# -- coding: utf-8 --
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(file))))
from ops import pexels_fetcher as pf

QUERIES = {
 'cute_animals': ['cute cat', 'cute dog', 'cute puppy', 'kitten'],
 'anime': ['anime', 'cartoon animation', 'japanese animation'],
 'roblox': ['minecraft gameplay', 'video game', 'gaming setup'],
}

def fetch(topic, queries, take=3):
 base = os.path.join('library', topic)
 os.makedirs(base, exist_ok=True)
 count = 0
 for q in queries:
 try:
 us = pf.urls(q, per=6)
 except Exception as e:
 print(topic, q, 'ERR', str(e)[:80])
 continue
 for i, u in enumerate(us[:take]):
 fn = os.path.join(base, 'pex' + q.replace(' ', '') + '' + str(i) + '.mp4')
 if os.path.exists(fn):
 continue
 try:
 pf.download(u, fn)
 count += 1
 except Exception as e:
 print(topic, q, i, 'DL-ERR', str(e)[:80])
 print(topic, 'downloaded', count, 'to', base)
 return count

if name == 'main':
 for t, qs in QUERIES.items():
 fetch(t, qs)
