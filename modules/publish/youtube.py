# -- coding: utf-8 --
# modules/publish/youtube.py - Wrapper os_publish
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
MODULE = {
	'name': 'publish.youtube',
	'version': '1.0.0',
	'interface': 'publish(file, title, desc, channel) -> dict',
	'config_schema': { 'channel': 'str' },
	'deps': ['ops.os_publish']
}
def publish(file, title, desc, channel):
	from ops import os_publish as op
	op.set_channel(channel)
	if hasattr(op, 'publish'):
		return op.publish(file, title=title, description=desc)
	if hasattr(op, 'upload'):
		return op.upload(file, title, desc)
	return { 'ok': False, 'error': 'no publish method' }
def health():
	try:
		from ops import os_publish
		return True
	except Exception:
		return False
