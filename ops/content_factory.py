# content_factory.py - merge fact_bank into content_db (dedup by id)
import os, sys, json
sys.path.insert(0, os.getcwd())
from ops import fact_bank as FB
DB = os.path.join(os.getcwd(), 'memory', 'content_db.json')

def merge():
 d = json.load(open(DB, encoding='utf-8'))
 have = set(it.get('id') for k in d for it in d[k])
 news = [f for f in FB.FACTS if f['id'] not in have]
 d.setdefault('facts', []).extend(news)
 json.dump(d, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
 return len(news), {k: len(v) for k, v in d.items()}

if __name__ == '__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8')
 print(merge())
