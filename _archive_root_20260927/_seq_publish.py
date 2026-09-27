# -- coding: utf-8 --
import os, sys, time, importlib
sys.path.insert(0, os.getcwd())
cl = importlib.import_module('ops.channel_loader')
cs = importlib.import_module('ops.channel_style')
cf = importlib.import_module('ops.content_freshness')
op = importlib.import_module('ops.os_publish')
load_content = getattr(cl, 'load_content')
load_cfg = getattr(cl, 'load')
build = getattr(cs, 'build_styled')
set_ch = getattr(cf, 'set_channel')
sig = getattr(cf, 'signature')
is_pub = getattr(cf, 'is_published')
op_set = getattr(op, 'set_channel')
op_pub = getattr(op, 'publish')
PLAN = {
	'Mialinhcute': ['anime', 'roblox', 'cute_animals', 'gacha'],
	'vilevi5676': ['facts', 'food', 'animals', 'whatif'],
}
def run():
	for channel, kinds in PLAN.items():
		print()
		print('===== ' + channel + ' =====')
		cfg = load_cfg(channel)
		style = cfg.get('style', {})
		style.setdefault('aspect', '9:16')
		set_ch(channel)
		op_set(channel)
		for kind in kinds:
			print()
			print('[kind] ', kind)
			items = load_content(channel, kind)
			print(' items: ', len(items))
			fresh = [it for it in items if not is_pub(sig(it, kind))]
			if not fresh:
				print(' -> het content, skip')
				continue
			it = fresh[0]
			vid = it.get('id')
			out = os.path.abspath(os.path.join('output', 'ch' + channel + '_' + kind + '_' + vid + '_' + time.strftime('%Y%m%d_%H%M%S') + '.mp4'))
			print(' render -> ', os.path.basename(out))
			try:
				build(it, out, style=style)
			except Exception as e:
				print(' build ERR: ', str(e)[:200])
				continue
			print(' size: ', os.path.getsize(out))
			print(' -> publish YouTube...')
			try:
				res = op_pub(out, (it.get('hook') or 'Video')[:100], description='', tags=None, privacy='public', topic=kind)
				print(' PUBLISH: ', res)
			except Exception as e:
				print(' pub ERR: ', str(e)[:200])

if __name__ == '__main__':
	run()
