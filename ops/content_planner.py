# -- coding: utf-8 --
"TNT Media OS - load Vietnamese scripts per topic."
import os, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'config', 'scripts_vi.json')

def _load():
    try:
        return json.load(open(SCRIPTS, encoding='utf-8'))
    except Exception:
        return dict()

def for_topic(topic):
    d = _load().get((topic or '').lower())
    if not d:
        return None, [], []
    hook = d.get('hook')
    lines = list(d.get('lines') or [])
    return hook, lines, lines

def has(topic):
    return (topic or '').lower() in _load()