import sys, os, json, time
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
import ops.channel_render as CR
from ops import quality_gate as QG
from ops import os_publish as OP
def pub(cid, out, hook):
	OP.set_channel(cid)
	title = hook[:90] + ' #shorts'
	tags = ['shorts', 'viral', 'khampha']
	desc = hook + chr(10) + chr(10) + ' '.join(['#'+t for t in tags])
	r = OP.publish(out, title, desc, tags=tags, privacy='unlisted', topic=cid+'test'+str(int(time.time())), force=True)
	return r.get('url') or r.get('error')
def process(cid, it):
	it = dict(it)
	oid = str(it.get('id')) + 't'
	it['id'] = oid
	out = 'output/' + cid + '' + oid + '.mp4'
	r = CR.render_for(cid, it, out, scenes=6)
	ok = isinstance(r, str) and os.path.exists(r)
	q = QG.evaluate(r) if ok else {}
	url = pub(cid, out, it.get('hook', '')) if (ok and q.get('passes')) else None
	return (cid, oid, ok, q.get('score'), url)
d1 = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
mia = [it for k in ['anime', 'roblox', 'cute_animals'] for it in d1.get(k, [])[:2]][:5]
d2 = json.load(open('channels/vilevi5676/content_db.json', encoding='utf-8'))
vile = [it for k in ['food', 'lifestyle', 'whatif', 'facts', 'animals'] for it in d2.get(k, [])[:1]][:5]
res = [process('Mialinhcute', it) for it in mia] + [process('vilevi5676', it) for it in vile]
zz = [print(r) for r in res]
print('ALL DONE', len(res))
