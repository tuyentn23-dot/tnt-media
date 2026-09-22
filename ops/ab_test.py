# ab_test.py - A/B hook test + tracking (tab)
import os, sys, json, time
sys.path.insert(0, os.getcwd())
from ops import ffmpeg_render as FR
from ops import hook_optimizer as HO
ROOT = os.getcwd()
ABLOG = os.path.join(ROOT, 'memory', 'ab_tests.json')

def log_ab(item_id, hook, video_id, url):
	d = json.load(open(ABLOG, encoding='utf-8')) if os.path.exists(ABLOG) else []
	d.append({'id': item_id, 'hook': hook, 'video_id': video_id, 'url': url, 'ts': time.strftime('%Y-%m-%d %H:%M')})
	json.dump(d, open(ABLOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
	return len(d)

def variants(item, n=2):
	return HO.best_hook(item, n)
