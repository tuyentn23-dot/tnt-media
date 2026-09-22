# channel_cli.py - CLI to manage channels.
import os, sys, io, json, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from ops import channel_loader as ch


def cmd_list(args):
	ids = ch.list_channels()
	print('Channels (', len(ids), '):')
	for cid in ids:
		try:
			cfg = ch.load(cid)
			en = cfg.get('enabled')
			kinds = cfg.get('content', {}).get('kinds', [])
			print(' -', cid, '|', cfg['name'], '| enabled=', en, '| kinds=', kinds)
		except Exception as e:
			print(' -', cid, 'ERROR:', e)


def cmd_add(args):
	cid = args.id
	if not cid or not cid.replace('_', '').replace('-', '').isalnum():
		print('invalid id: use alphanumeric + _ -')
		return
	try:
		dst = ch.create_from_template(cid, name=args.name, token_file=args.token)
		print('created:', dst)
		print('next: edit channel.json, add content_db.json + token.pickle')
	except Exception as e:
		print('ERROR:', e)


def cmd_set_enabled(args):
	cid = args.id
	cfg = ch.load(cid)
	cfg['enabled'] = args.flag.lower() in ('1', 'true', 'yes', 'on')
	ch.save(cid, cfg)
	print(cid, 'enabled =', cfg['enabled'])


def cmd_show(args):
	cfg = ch.load(args.id)
	print(json.dumps(cfg, ensure_ascii=False, indent=2))


def cmd_token(args):
	cfg = ch.load(args.id)
	tp = ch.token_path(cfg)
	print('token path:', tp, 'exists=', os.path.exists(tp))


def main():
	ap = argparse.ArgumentParser(prog='channel_cli')
	sub = ap.add_subparsers(dest='cmd')
	p = sub.add_parser('list')
	p.set_defaults(fn=cmd_list)
	p = sub.add_parser('add')
	p.add_argument('id')
	p.add_argument('--name', default=None)
	p.add_argument('--token', default=None)
	p.set_defaults(fn=cmd_add)
	p = sub.add_parser('enable')
	p.add_argument('id')
	p.add_argument('flag', nargs='?', default='true')
	p.set_defaults(fn=cmd_set_enabled)
	p = sub.add_parser('show')
	p.add_argument('id')
	p.set_defaults(fn=cmd_show)
	p = sub.add_parser('token')
	p.add_argument('id')
	p.set_defaults(fn=cmd_token)
	args = ap.parse_args()
	if not getattr(args, 'fn', None):
		ap.print_help()
		return
	args.fn(args)


if __name__ == '__main__':
	main()
