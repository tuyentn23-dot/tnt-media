# -- coding: utf-8 --
# modules/content/loader.py - Load content items cho channel
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

MODULE = {
	'name': 'content.loader',
	'version': '1.0.0',
	'interface': 'load(channel_id, kind) -> list[dict]',
	'config_schema': {'channel_id': 'str', 'kind': 'str'},
	'deps': [],
	'health': 'True'
}


def load(channel_id, kind=None):
	from ops import channel_loader as ch
	if kind:
		return ch.load_content(channel_id, kind)
	cfg = ch.load(channel_id)
	kinds = cfg.get('content', {}).get('kinds', [])
	out = []
	for k in kinds:
		out.extend(ch.load_content(channel_id, k))
	return out


def health():
	try:
		from ops import channel_loader
		return True
	except Exception:
		return False
