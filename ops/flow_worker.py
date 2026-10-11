# ops/flow_worker.py - Chay flow_video trong subprocess rieng
# De co the kill process khi timeout (khong bi treo Playwright)
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
	prompt = payload.get('prompt', '')
	out = payload.get('out', '')
	wait = int(payload.get('wait', 240))
	aspect = payload.get('aspect', '9:16')
	if not prompt or not out:
		print(json.dumps({'ok': False, 'error': 'prompt/out required'}))
		return 2
	try:
		from modules.render import flow_video as fv
		r = fv.create(prompt, out, wait=wait, aspect=aspect)
		print(json.dumps(r, ensure_ascii=False))
		return 0 if r.get('ok') else 3
	except Exception as e:
		import traceback
		print(json.dumps({'ok': False, 'error': 'worker ex: ' + str(e)[:200], 'trace': traceback.format_exc()[-500:]}))
		return 4


if __name__ == '__main__':
	sys.exit(main())
