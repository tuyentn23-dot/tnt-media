# ops/gacha_worker.py - Chay render_gacha trong subprocess (kill duoc khi timeout)
import os, sys, json, argparse
os.environ.setdefault('PYTHONUTF8', '1')
try:
	sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
	pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('--json', required=True)
	args = ap.parse_args()
	try:
		payload = json.loads(args.json)
	except Exception as e:
		print(json.dumps({'ok': False, 'error': 'parse json: ' + str(e)[:150]}))
		return 1
	item = payload.get('item') or {}
	out = payload.get('out', '')
	voice = payload.get('voice', 'female_north')
	preset = payload.get('preset', 'cute')
	seed = payload.get('seed')
	if not out:
		print(json.dumps({'ok': False, 'error': 'out required'}))
		return 2
	try:
		from ops import ffmpeg_render as fr
		r = fr.render_gacha(item, out, voice=voice, preset=preset, seed=seed)
		if isinstance(r, tuple):
			print(json.dumps({'ok': False, 'error': 'ffmpeg fail: ' + str(r[1])[:200]}))
			return 3
		ok = os.path.exists(out)
		print(json.dumps({'ok': ok, 'path': out if ok else None, 'error': None if ok else 'no file'}))
		return 0 if ok else 4
	except Exception as e:
		import traceback
		print(json.dumps({'ok': False, 'error': 'worker ex: ' + str(e)[:200], 'trace': traceback.format_exc()[-500:]}))
		return 5


if __name__ == '__main__':
	sys.exit(main())
