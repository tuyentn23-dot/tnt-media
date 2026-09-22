# -- coding: utf-8 --
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(file))))
from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish

CID = 'Mialinhcute'

def main():
 cfg = ch.load(CID)
 style = cfg.get('style', {})
 kinds = cfg.get('content', {}).get('kinds', ['anime', 'roblox', 'cute_animals'])
 cf.set_channel(CID)
 os_publish.set_channel(CID)
 picks = []
 for kind in kinds:
 items = ch.load_content(CID, kind)
 fresh = [it for it in items if not cf.is_published(cf.signature(it, kind))]
 picks.extend([(kind, it) for it in fresh[:2]])
 results = []
 for kind, item in picks[:4]:
 out = os.path.abspath('output/ch' + CID + '' + item['id'] + '' + time.strftime('%Y%m%d_%H%M%S') + '.mp4')
 os.makedirs(os.path.dirname(out), exist_ok=True)
 cs.build_styled(item, out, style=style)
 c = cfg.get('content', {})
 fmt = {k: item.get(k, '') for k in ['hook', 'body', 'payoff', 'id', 'topic']}
 title = c.get('title_template', '{hook}').format(fmt)[:100]
 desc = c.get('desc_template', '{body} {payoff}').format(fmt)[:450]
 tags = list(c.get('tags_base', [])) + [item.get('topic', ''), CID]
 topic = 'ch' + CID + '' + kind + '' + item['id']
 res = os_publish.publish(out, title, description=desc, tags=tags, privacy='public', topic=topic, category_id=str(c.get('category_id', '24')), force=True)
 sig = cf.signature(item, kind)
 cf.mark_published(sig, {'youtube_id': res.get('youtube_id') if isinstance(res, dict) else None, 'topic': topic, 'kind': kind, 'file': out})
 results.append({'kind': kind, 'id': item['id'], 'title': title, 'res': res})
 print('PUBLISHED', kind, item['id'], res.get('youtube_id') if isinstance(res, dict) else res)
 print('DONE', len(results))
 return results

if name == 'main':
 main()
