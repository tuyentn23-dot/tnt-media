# channel_pipeline.py - Run PDCA pipeline for ONE channel.
import os, sys, io, json, time, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish


def _lock_path(cid):
	d = ch.channel_dir(cid)
	os.makedirs(d, exist_ok=True)
	return os.path.join(d, '_pipeline.lock')


def _pid_alive(pid):
	try:
		r = subprocess.run(['tasklist', '/FI', 'PID eq ' + str(pid), '/NH'], capture_output=True, text=True)
		return str(pid) in r.stdout
	except Exception:
		return False


def _acquire(cid):
	p = _lock_path(cid)
	if os.path.exists(p):
		try:
			oldpid = int(io.open(p).read().strip())
		except Exception:
			oldpid = 0
		if oldpid and _pid_alive(oldpid):
			print('LOCKED channel', cid, 'pid', oldpid)
			return False
		print('stale lock', cid, 'removing')
		os.remove(p)
	io.open(p, 'w').write(str(os.getpid()))
	return True


def release(cid):
	p = _lock_path(cid)
	if os.path.exists(p):
		os.remove(p)


def resolve_items(cfg, kind):
	items = ch.load_content(cfg['id'], kind)
	if items:
		return items
	try:
		from ops.content_video5 import load as legacy
		return legacy(kind)
	except Exception:
		return []


def publish_one(cid, cfg, item, kind):
	style = cfg.get('style', {})
	out = os.path.abspath('output/ch' + cid + '' + item['id'] + '.mp4')
	os.makedirs(os.path.dirname(out), exist_ok=True)
	cs.build_styled(item, out, style=style)
	title = (item.get('hook') or item.get('title') or item['id'])[:90]
	c = cfg.get('content', {})
	tt = c.get('title_template', '{hook}')
	dt = c.get('desc_template', '{body} {payoff}')
	fmt = {k: item.get(k, '') for k in ['hook', 'body', 'payoff', 'id', 'topic']}
	try:
		title = tt.format(fmt)[:100]
	except Exception:
		pass
	try:
		desc = dt.format(fmt)[:450]
	except Exception:
		desc = (item.get('body', '') + ' ' + item.get('payoff', ''))[:450]
	tags = list(c.get('tags_base', [])) + [item.get('topic', ''), cid]
	topic = 'ch' + cid + '' + kind + '' + item['id']
	os_publish.set_channel(cid)
	res = os_publish.publish(out, title, description=desc, tags=tags, privacy='public',
		topic=topic, category_id=str(c.get('category_id', '24')), force=True)
	sig = cf.signature(item, kind)
	cf.mark_published(sig, {'youtube_id': res.get('youtube_id') if isinstance(res, dict) else None,
		'topic': topic, 'kind': kind, 'file': out})
	print('PUBLISHED', cid, item['id'], res.get('youtube_id') if isinstance(res, dict) else res)
	return res


def run_channel(cid, batch=None):
	cfg = ch.load(cid)
	if not cfg.get('enabled', False):
		print('channel disabled:', cid)
		return {'ok': False, 'reason': 'disabled'}
	if not _acquire(cid):
		return {'ok': False, 'reason': 'locked'}
	try:
		cf.set_channel(cid)
		os_publish.set_channel(cid)
		sched = cfg.get('schedule', {})
		limit = int(batch if batch is not None else sched.get('batch', 2))
		kinds = cfg.get('content', {}).get('kinds', ['whatif'])
		n = 0
		for kind in kinds:
			if n >= limit:
				break
			items = resolve_items(cfg, kind)
			for it in items:
				if n >= limit:
					break
				sig = cf.signature(it, kind)
				if cf.is_published(sig):
					print('SKIP', cid, kind, it['id'])
					continue
				try:
					publish_one(cid, cfg, it, kind)
					n += 1
				except Exception as e:
					print('ERR', cid, it['id'], str(e)[:200])
		print('DONE', cid, 'published', n, 'ledger', cf.published_count())
		return {'ok': True, 'published': n, 'ledger': cf.published_count()}
	finally:
		release(cid)


def main():
	if len(sys.argv) < 2:
		print('usage: python -m ops.channel_pipeline <channel_id> [batch]')
		return
	cid = sys.argv[1]
	batch = int(sys.argv[2]) if len(sys.argv) > 2 else None
	r = run_channel(cid, batch=batch)
	print('RESULT', r)


if __name__ == '__main__':
	main()
