# publish_studio.py - upload rendered videos from manifest (flat)
import os, sys, json, time
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP

ROOT = os.getcwd()
MANIFEST = os.path.join(ROOT, 'memory', 'render_manifest.json')
PUBSTATE = os.path.join(ROOT, 'memory', 'publish_studio_state.json')

HASHTAGS = ['#shorts', '#viral', '#khampha', '#suthat', '#khoahoc']
def load_state():
 return json.load(open(PUBSTATE, encoding='utf-8')) if os.path.exists(PUBSTATE) else {'published': []}

def save_state(s):
 json.dump(s, open(PUBSTATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def build_meta(r):
 hook = r.get('hook', '').strip().rstrip('.')
 title = (hook[:90] + ' #shorts') if hook else ('Kham pha thu vi #shorts')
 tags = ' '.join(HASHTAGS)
 desc = hook + chr(10) + chr(10) + tags
 return title, desc

def publish_manifest(channel=None, privacy='public', limit=99, only_ok=True):
 m = json.load(open(MANIFEST, encoding='utf-8'))
 st = load_state()
 done = set(st.get('published', []))
 items = [r for r in m.get('results', []) if (not only_ok or r.get('ok')) and r.get('out') and r['out'] not in done][:limit]
 outs = [publish_one(r, privacy) for r in items]
 st['published'] = list(done) + [r['out'] for r in items]
 save_state(st)
 return outs

def publish_one(r, privacy):
 title, desc = build_meta(r)
 vid = r['out'] if os.path.isabs(r['out']) else os.path.join(ROOT, r['out'])
 res = OP.publish(vid, title, desc, tags=HASHTAGS, privacy=privacy, topic=r.get('topic', ''))
 return (r['id'], res.get('ok'), str(res.get('video_id') or res.get('error'))[:60])
if __name__ == '__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8')
 outs = publish_manifest(limit=1)
 _ = [print(o) for o in outs]
