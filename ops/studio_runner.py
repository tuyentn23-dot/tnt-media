# studio_runner.py - batch render + health check + manifest (flat)
import os, sys, json, time, hashlib
try:
	sys.stdout.reconfigure(encoding="utf-8")
except Exception:
	pass
sys.path.insert(0, os.getcwd())
from ops import ffmpeg_render as FR
from ops import video_health as VH
from ops import thumbnail as TH

ROOT = FR.ROOT
DB = os.path.join(ROOT, 'memory', 'content_db.json')
OUT = os.path.join(ROOT, 'output')
MANIFEST = os.path.join(ROOT, 'memory', 'render_manifest.json')
def load_db():
 return json.load(open(DB, encoding='utf-8'))

def save_manifest(m):
 json.dump(m, open(MANIFEST, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def render_one(item, tag=''):
 cid = str(item.get('id', 'x')) + tag
 it = dict(item); it['id'] = cid
 out = os.path.join(OUT, 'v_' + cid + '.mp4')
 t0 = time.time()
 r = FR.render(it, out, seed=None)
 dt = round(time.time() - t0, 1)
 ok = isinstance(r, str) and os.path.exists(r) and os.path.getsize(r) > 5000
 health = VH.check(r) if ok else {'ok': False}
 thumb = (TH.make(r, item.get('hook', ''), os.path.join(OUT, 'thumb_' + cid + '.jpg'), t=1.2) if ok else None)
 return {'id': cid, 'out': r, 'ok': ok, 'sec': dt, 'thumb': thumb, 'health': health, 'topic': item.get('topic', ''), 'hook': item.get('hook', '')}
def run_batch(kinds=None, limit=2):
 db = load_db()
 kinds = kinds or list(db.keys())
 jobs = [(k, it) for k in kinds for it in db.get(k, [])[:limit]]
 results = [render_one(it, tag='_'+k) for (k, it) in jobs]
 save_manifest({'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'results': results})
 return results




if __name__ == '__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8')
 res = run_batch(limit=2)
 okn = sum(1 for r in res if r['ok'])
 print('RENDERED ', okn, '/', len(res))
 _ = [print(r['id'], r['ok'], r['sec'], r['health'].get('ok')) for r in res]
