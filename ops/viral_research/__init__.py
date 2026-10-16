# -- coding: utf-8 --
# ops/viral_research/init.py
# Module nghien cuu video viral da nen tang (metadata only, khong tai video).
import os, json, time, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()['__file__']))))
OUT = os.path.join(ROOT, 'analytics', 'trending')


def _ensure():
	os.makedirs(OUT, exist_ok=True)


def run_youtube(region='VN', max_results=30):
	from . import youtube as yt
	from . import patterns as pt
	r = yt.via_api(region=region, max_results=max_results)
	if not r.get('ok'):
		return r
	summary = pt.summarize(r['items'])
	return {'ok': True, 'items': r['items'], 'summary': summary, 'region': region}


def run_search(query, max_results=20, platform='youtube', shorts=True):
	from . import youtube as yt
	from . import patterns as pt
	q = (query + ' shorts') if shorts else query
	r = yt.search(q, max_results=max_results, platform=platform)
	if not r.get('ok'):
		return r
	items = r['items']
	if shorts:
		items = yt.only_shorts(items)
	summary = pt.summarize(items)
	return {'ok': True, 'items': items, 'summary': summary, 'query': query, 'platform': platform, 'shorts_filtered': bool(shorts)}


def run_hashtag(platform, tag, max_results=15):
	from . import social as so
	from . import patterns as pt
	r = so.search_hashtag(platform, tag, max_results=max_results)
	if not r.get('ok'):
		return r
	summary = pt.summarize(r['items'])
	return {'ok': True, 'items': r['items'], 'summary': summary, 'platform': platform, 'tag': tag}


def save(result, name=''):
	_ensure()
	ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	fn = (name or 'trending') + '_' + ts + '.json'
	p = os.path.join(OUT, fn)
	json.dump(result, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
	return p


def latest(n=3):
	_ensure()
	fs = sorted([f for f in os.listdir(OUT) if f.endswith('.json')], reverse=True)
	out = []
	for f in fs[:n]:
		try:
			out.append(json.load(open(os.path.join(OUT, f), encoding='utf-8')))
		except Exception:
			pass
	return out


if globals()['__name__'] == '__main__':
	import sys
	args = sys.argv[1:]
	if not args:
		print('usage: python -m ops.viral_research youtube | search <query> | hashtag <platform> <tag>')
		sys.exit(1)
	cmd = args[0]
	if cmd == 'youtube':
		r = run_youtube()
	elif cmd == 'search':
		r = run_search(' '.join(args[1:]), max_results=15)
	elif cmd == 'hashtag' and len(args) >= 3:
		r = run_hashtag(args[1], args[2])
	else:
		print('unknown cmd')
		sys.exit(1)
	if r.get('ok'):
		p = save(r, name=cmd)
		print('OK saved:', p)
		print('summary:', json.dumps(r.get('summary'), ensure_ascii=False, indent=2)[:600])
	else:
		print('FAIL:', r.get('error'))
