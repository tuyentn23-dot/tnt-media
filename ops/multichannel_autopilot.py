# multichannel_autopilot.py - Run channel_pipeline for every enabled channel.
import os, sys, io, json, time, subprocess, threading
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from ops import channel_loader as ch

PY = sys.executable
LOG = os.path.join(ROOT, 'memory', 'multichannel_log.jsonl')
CFG = os.path.join(ROOT, 'memory', 'multichannel.json')


def _default_cfg():
	return {'enabled': False, 'interval_min': 60, 'channels': []}


def load_cfg():
	try:
		return json.load(io.open(CFG, encoding='utf-8'))
	except Exception:
		return _default_cfg()


def save_cfg(c):
	io.open(CFG, 'w', encoding='utf-8').write(json.dumps(c, ensure_ascii=False, indent=2))


def _log(ev):
	ev['ts'] = time.strftime('%Y-%m-%dT%H:%M:%S')
	io.open(LOG, 'a', encoding='utf-8').write(json.dumps(ev, ensure_ascii=False) + chr(10))


def active_channels():
	cfg = load_cfg()
	explicit = cfg.get('channels') or []
	if explicit:
		return [c for c in explicit if os.path.isdir(ch.channel_dir(c))]
	return ch.list_channels(include_disabled=False)


def run_all():
	ids = active_channels()
	results = []
	for cid in ids:
		try:
			r = subprocess.run([PY, '-X', 'utf8', '-m', 'ops.channel_pipeline', cid],
				cwd=ROOT, capture_output=True, text=True, timeout=3600)
			out = (r.stdout or '')[-1500:]
			res = {'channel': cid, 'rc': r.returncode, 'out': out}
			results.append(res)
			_log({'event': 'channel_done', **res})
		except Exception as e:
			results.append({'channel': cid, 'error': str(e)[:200]})
			_log({'event': 'channel_error', 'channel': cid, 'err': str(e)[:200]})
	return results


_stop = threading.Event()
_thread = None


def _loop():
	while not _stop.is_set():
		cfg = load_cfg()
		if cfg.get('enabled'):
			try:
				run_all()
			except Exception as e:
				_log({'event': 'error', 'err': str(e)[:200]})
		iv = max(5, int(cfg.get('interval_min', 60))) * 60
		_stop.wait(iv)


def start():
	global _thread
	if _thread and _thread.is_alive():
		return False
	_stop.clear()
	_thread = threading.Thread(target=_loop, daemon=True)
	_thread.start()
	_log({'event': 'multichannel_started'})
	return True


def stop():
	_stop.set()
	_log({'event': 'multichannel_stopped'})
	return True


def set_enabled(flag):
	c = load_cfg()
	c['enabled'] = bool(flag)
	save_cfg(c)
	if flag:
		start()
	return c


def status():
	c = load_cfg()
	return {'enabled': c.get('enabled'), 'interval_min': c.get('interval_min'),
		'channels_active': active_channels(), 'running': bool(_thread and _thread.is_alive())}


if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'run':
		print(json.dumps(run_all(), ensure_ascii=False, indent=2))
	elif len(sys.argv) > 2 and sys.argv[1] == 'enable':
		print(set_enabled(sys.argv[2].lower() in ('1', 'true', 'yes', 'on')))
	else:
		print(json.dumps(status(), ensure_ascii=False, indent=2))
