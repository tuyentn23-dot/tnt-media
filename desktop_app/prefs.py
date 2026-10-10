# desktop_app/prefs.py - Luu/tai preferences
import os, json
_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_DIR)
PATH = os.path.join(ROOT, 'state', 'desktop_prefs.json')

DEFAULTS = {
	'last_tab': 0,
	'lang': 'vi',
	'theme': 'light',
	'geometry': None,
}


def load():
	try:
		if os.path.exists(PATH):
			d = json.load(open(PATH, encoding='utf-8'))
			for k in DEFAULTS:
				if k not in d:
					d[k] = DEFAULTS[k]
			return d
	except Exception:
		pass
	return dict(DEFAULTS)


def save(data):
	try:
		os.makedirs(os.path.dirname(PATH), exist_ok=True)
		json.dump(data, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
		return True
	except Exception:
		return False
