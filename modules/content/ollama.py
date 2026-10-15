# tool: content-ollama
# -- coding: utf-8 --
# modules/content/ollama.py - Sinh noi dung bang Ollama
import os, sys
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'content-ollama',
	'name': 'content.ollama',
	'version': '1.0.0',
	'interface': 'generate(topic, kind, channel) -> dict',
	'deps': ['ops.ai_content']
}


def generate(topic, kind='default', channel=None):
	from ops import ai_content as ac
	return ac.generate(topic=topic, kind=kind)
