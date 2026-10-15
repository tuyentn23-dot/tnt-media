# tool: content-manual
# -- coding: utf-8 --
# modules/content/manual.py - Sinh noi dung theo yeu cau (prompt thu cong)
import os, sys
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'content-manual',
	'name': 'content.manual',
	'version': '1.0.0',
	'interface': 'generate(prompt, channel=None) -> dict',
	'deps': ['ops.ai_content']
}


def generate(prompt, channel=None):
	from ops import ai_content as ac
	return ac.generate(topic=prompt, kind='manual')
