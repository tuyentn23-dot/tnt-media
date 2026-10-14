# -- coding: utf-8 --
# modules/render/flow_video.py v7.0.0 - Google Flow Veo WORKING end-to-end
# Workflow: new_project -> submit -> approve -> wait_tile -> open_editor -> download
import os, sys, time, base64, re as _re
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)
MODULE = {
	'name': 'render.flow_video',
	'version': '7.1.0',
	'interface': 'create(prompt, out_path, wait=900) -> dict',
	'config_schema': {'aspect': 'str'},
	'deps': ['playwright']
}
CDP = os.environ.get('TNT_CDP', 'http://127.0.0.1:9222')
ASPECT = os.environ.get('TNT_FLOW_ASPECT', '9:16')
QUALITY = os.environ.get('TNT_FLOW_QUALITY', '720p')


def log(m):
	try:
		print('[flow] ' + str(m), flush=True)
	except Exception:
		pass


def connect():
	from playwright.sync_api import sync_playwright
	p = sync_playwright().start()
	b = p.chromium.connect_over_cdp(CDP)
	return p, b, b.contexts[0]


def pick_page(ctx):
	for x in ctx.pages:
		if 'flow.google.com' in x.url:
			return x
	return None


APPROVE_B64 = 'KCkgPT4geyBjb25zdCBzcGFucyA9IFsuLi5kb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCdzcGFuLm9wdGlvbi1sYWJlbCcpXTsgZm9yIChjb25zdCBzIG9mIHNwYW5zKSB7IGNvbnN0IHQgPSAocy5pbm5lclRleHR8fCcnKS50cmltKCk7IGlmICh0ID09PSAnQWx3YXlzIGFwcHJvdmUnIHx8IHQgPT09ICdBcHByb3ZlJykgeyBjb25zdCBwID0gcy5jbG9zZXN0KCdidXR0b24sIFtyb2xlPWJ1dHRvbl0sIFtyb2xlPW1lbnVpdGVtXSwgbGksIGRpdicpOyBpZiAocCkgeyBwLmNsaWNrKCk7IHJldHVybiAnY2xpY2tlZCAnICsgdDsgfSBzLmNsaWNrKCk7IHJldHVybiAnY2xpY2tlZCBzcGFuICcgKyB0OyB9IH0gcmV0dXJuIG51bGw7IH0='
DOWNLOAD_B64 = 'KCkgPT4geyBjb25zdCBpY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJ21hdC1pY29uJyk7IGZvciAoY29uc3QgaWMgb2YgaWNvbnMpIHsgaWYgKChpYy5pbm5lclRleHR8fCcnKS50cmltKCkgPT09ICdkb3dubG9hZCcpIHsgY29uc3QgYnRuID0gaWMuY2xvc2VzdCgnYnV0dG9uJyk7IGlmIChidG4pIHsgYnRuLmNsaWNrKCk7IHJldHVybiAnY2xpY2tlZCBkb3dubG9hZCc7IH0gfSB9IHJldHVybiAnbm90Zm91bmQnOyB9'
QUALITY_B64 = 'KHEpID0+IHsgY29uc3QgZWxzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnKicpOyBsZXQgYmVzdD1udWxsOyBsZXQgYmxlbj0xZTk7IGZvciAoY29uc3QgZSBvZiBlbHMpIHsgY29uc3QgdD0oZS5pbm5lclRleHR8fCcnKS50cmltKCk7IGlmICh0LnN0YXJ0c1dpdGgocSkgJiYgdC5sZW5ndGggPCBibGVuKSB7IGJlc3Q9ZTsgYmxlbj10Lmxlbmd0aDsgfSB9IGlmIChiZXN0KSB7IGJlc3QuY2xpY2soKTsgcmV0dXJuICdjbGlja2VkICcgKyBxOyB9IHJldHVybiAnbm90Zm91bmQnOyB9'


def click_approve_if_present(pg):
	# Flow UI moi: span.option-label Approve/Always approve -> click qua locator
	try:
		spans = pg.locator('span.option-label')
		n = spans.count()
		for i in range(n):
			try:
				txt = (spans.nth(i).inner_text() or '').strip()
				if txt in ('Always approve', 'Approve'):
					spans.nth(i).click(timeout=3000, force=True)
					log('approve clicked: ' + txt)
					return 'clicked ' + txt
			except Exception:
				continue
	except Exception as e:
		log('approve ex: ' + str(e)[:80])
	# Fallback JS cu
	try:
		js = base64.b64decode(APPROVE_B64).decode()
		return pg.evaluate(js)
	except Exception as e:
		return None

def click_download_icon(pg):
	js = base64.b64decode(DOWNLOAD_B64).decode()
	return pg.evaluate(js)


def click_quality(pg, quality):
	js = base64.b64decode(QUALITY_B64).decode()
	return pg.evaluate(js, quality)


def dismiss_promo(pg):
	try:
		for sel in ['[aria-label=Close]', '[aria-label="Close"]', 'button[aria-label=close]', '[data-test-id=close]']:
			el = pg.locator(sel).first
			if el.count() > 0:
				el.click(timeout=2000)
				log('closed promo: ' + sel)
				time.sleep(0.5)
	except Exception:
		pass

def new_project(pg):
	try:
		pg.goto('https://flow.google.com/', wait_until='domcontentloaded', timeout=30000)
		time.sleep(5)
	except Exception:
		pass
	dismiss_promo(pg)
	time.sleep(1)
	clicked = False
	try:
		btns = pg.locator('button')
		n = btns.count()
		for i in range(n):
			try:
				txt = (btns.nth(i).inner_text() or '').strip()
				if 'New project' in txt:
					btns.nth(i).click(timeout=8000, force=True)
					clicked = True
					log('clicked New project idx=' + str(i))
					break
			except Exception:
				continue
	except Exception:
		pass
	if clicked:
		for _ in range(30):
			time.sleep(1)
			if '/project/' in pg.url:
				break
	return {'clicked': clicked, 'url': pg.url}


def find_button_by_text(pg, text):
	btns = pg.locator('button')
	n = btns.count()
	for i in range(n):
		try:
			txt = (btns.nth(i).inner_text() or '').strip()
			if txt == text:
				return btns.nth(i)
		except Exception:
			pass
	return None


def submit_prompt(pg, prompt):
	inp = None
	for _ in range(15):
		inp = pg.locator('.ProseMirror')
		if inp.count() > 0:
			break
		inp = pg.locator('[contenteditable=true]')
		if inp.count() > 0:
			break
		time.sleep(2)
	if not inp or inp.count() == 0:
		return {'ok': False, 'err': 'no input'}
	inp.last.focus(timeout=15000)
	time.sleep(1)
	try:
		pg.keyboard.press('Control+A')
		pg.keyboard.press('Delete')
	except Exception:
		pass
	p2 = prompt
	low = p2.lower()
	if not (low.startswith('generate a video') or low.startswith('create a video')):
		p2 = 'Generate a video: ' + p2
	if '9:16' not in p2 and 'vertical' not in p2.lower():
		p2 = p2 + ', vertical 9:16 portrait'
	pg.keyboard.type(p2, delay=15)
	time.sleep(1)
	sb = find_button_by_text(pg, 'arrow_forward')
	if sb:
		sb.click(timeout=5000)
		return {'ok': True}
	return {'ok': False, 'err': 'no submit button'}


def wait_video_tile(pg, wait, stall_limit=120):
	t0 = time.time()
	last_tiles = 0
	last_change = time.time()
	while time.time() - t0 < wait:
		time.sleep(10)
		try:
			ap = click_approve_if_present(pg)
			if ap:
				log('approve: ' + str(ap))
			tiles = pg.locator('flow-video-tile').count()
			log('wait t=' + str(int(time.time()-t0)) + ' tiles=' + str(tiles) + ' stall=' + str(int(time.time()-last_change)))
			if tiles != last_tiles:
				last_tiles = tiles
				last_change = time.time()
			if (time.time() - last_change) > stall_limit:
				log('STALL: abort after ' + str(stall_limit) + 's no progress')
				return {'ok': False, 'err': 'stall ' + str(stall_limit) + 's'}
			if tiles > 0:
				time.sleep(15)
				tiles2 = pg.locator('flow-video-tile').count()
				if tiles2 > 0:
					return {'ok': True, 'tiles': tiles2}
		except Exception as e:
			log('wait err: ' + str(e)[:80])
	return {'ok': False, 'err': 'timeout'}


def open_editor(pg):
	tiles = pg.locator('flow-video-tile')
	n = tiles.count()
	if n == 0:
		return {'ok': False, 'err': 'no tiles'}
	for idx in [n-1, 0]:
		try:
			ti = tiles.nth(idx)
			ti.scroll_into_view_if_needed(timeout=3000)
			time.sleep(1)
			bb = ti.bounding_box()
			if bb and bb.get('width', 0) > 0 and bb.get('height', 0) > 0:
				cx = bb['x'] + bb['width'] / 2
				cy = bb['y'] + bb['height'] / 2
				pg.mouse.click(cx, cy)
				time.sleep(6)
				return {'ok': True, 'url': pg.url, 'idx': idx}
		except Exception:
			continue
	return {'ok': False, 'err': 'no visible tile'}


def wait_download_enabled(pg, timeout=300):
	import time as _t
	t0 = _t.time()
	while _t.time() - t0 < timeout:
		try:
			btn = pg.locator('button[aria-label="Download media"]').first
			if btn.count() > 0 and not btn.is_disabled():
				return {'ok': True, 'waited': int(_t.time() - t0)}
		except Exception:
			pass
		_t.sleep(3)
	return {'ok': False, 'err': 'download still disabled'}


def download_video(pg, out_path, quality=None):
	quality = quality or QUALITY
	wd = wait_download_enabled(pg)
	log('dl-enabled: ' + str(wd))
	try:
		body = pg.evaluate("() => document.body.innerText")
		dialog_open = (quality in body) or ('Animated GIF' in body)
	except Exception:
		dialog_open = False
	try:
		with pg.expect_download(timeout=180000) as dl_info:
			if not dialog_open:
				r1 = click_download_icon(pg)
				log('dl icon: ' + str(r1))
				for _w in range(15):
					time.sleep(1)
					try:
						b2 = pg.evaluate("() => document.body.innerText")
						if "720p" in b2 or "1080p" in b2 or "Animated GIF" in b2:
							break
					except Exception:
						pass
				log("wait-dialog t=" + str(_w) + " has720=" + str("720p" in b2))
			else:
				log('dialog already open')
			r2 = click_quality(pg, quality)
			log('quality ' + quality + ': ' + str(r2))
		dl = dl_info.value
		os.makedirs(os.path.dirname(os.path.abspath(out_path)) or '.', exist_ok=True)
		dl.save_as(out_path)
		if os.path.exists(out_path):
			return {'ok': True, 'path': out_path, 'bytes': os.path.getsize(out_path)}
		return {'ok': False, 'err': 'no file'}
	except Exception as e:
		return {'ok': False, 'err': 'dl ex: ' + str(e)[:200]}


def _safe_stop(pw):
	try:
		pw.stop()
	except Exception:
		pass


def inner(prompt, out_path, wait, aspect):
	res = {'ok': False, 'path': None, 'error': None, 'steps': []}
	return _inner_impl(prompt, out_path, wait, aspect, res)


def _inner_impl(prompt, out_path, wait, aspect, res):
	p = None
	try:
		p, b, ctx = connect()
		return _inner_body(p, b, ctx, prompt, out_path, wait, aspect, res)
	finally:
		if p is not None:
			_safe_stop(p)


def _inner_body(p, b, ctx, prompt, out_path, wait, aspect, res):
	pg = pick_page(ctx)
	if pg is None:
		pg = ctx.new_page()
	pg.bring_to_front()
	# Luon quay ve home chat view (don gian nhat)
	try:
		if 'flow.google.com/project' in pg.url or '/edit/' in pg.url:
			pg.goto('https://flow.google.com/', wait_until='domcontentloaded', timeout=30000)
			time.sleep(5)
	except Exception:
		pass
	res['steps'].append('home ' + pg.url[:60])
	time.sleep(2)
	# Dam bao co input: neu khong co ProseMirror -> bam New project
	try:
		if pg.locator(".ProseMirror").count() == 0 and pg.locator("[contenteditable=true]").count() == 0:
			btns = pg.locator("button")
			n = btns.count()
			for i in range(n):
				try:
					if "New project" in (btns.nth(i).inner_text() or ""):
						btns.nth(i).click(timeout=8000, force=True)
						res["steps"].append("clicked-new-project")
						time.sleep(6)
						break
				except Exception:
					continue
	except Exception as _ne:
		res["steps"].append("newproj-ex " + str(_ne)[:80])
	# Submit prompt truc tiep tren chat view
	sp = submit_prompt(pg, prompt)
	res['steps'].append('submit ' + str(sp))
	if not sp.get('ok'):
		res['error'] = sp.get('err')
		return res
	# Wait video tile (auto approve credit)
	w = wait_video_tile(pg, wait)
	res['steps'].append('wait ' + str(w))
	if not w.get('ok'):
		res['error'] = 'no tile: ' + str(w.get('err'))
		return res
	time.sleep(2)
	# Mo editor neu chua
	if '/edit/' in pg.url:
		res['steps'].append('already-in-editor')
	else:
		oe = open_editor(pg)
		res['steps'].append('editor ' + str(oe))
		if not oe.get('ok'):
			res['error'] = 'no editor: ' + str(oe.get('err'))
			return res
	time.sleep(3)
	# Download
	dv = download_video(pg, out_path)
	res['steps'].append('download ' + str(dv))
	if dv.get('ok'):
		res['ok'] = True
		res['path'] = out_path
		return res
	res['error'] = dv.get('err')
	return res



def create_with_timeout(prompt, out_path, wait, aspect, hard_timeout):
	import subprocess, json, os, sys
	worker = os.path.join(ROOT, 'ops', 'flow_worker.py')
	if not os.path.exists(worker):
		return {'ok': False, 'path': None, 'error': 'flow_worker.py missing'}
	payload = {'prompt': prompt, 'out': out_path, 'wait': wait, 'aspect': aspect}
	cmd = [sys.executable, worker, '--json', json.dumps(payload, ensure_ascii=False)]
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	log_p = os.path.join(ROOT, 'logs', 'flow_worker.log')
	os.makedirs(os.path.dirname(log_p), exist_ok=True)
	try:
		f = open(log_p, 'a', encoding='utf-8')
		f.write(chr(10) + chr(61)*40 + chr(10))
		f.write('flow worker start: ' + str(out_path) + chr(10))
		f.flush()
		proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	except Exception as e:
		return {'ok': False, 'path': None, 'error': 'spawn worker fail: ' + str(e)[:200]}
	try:
		proc.wait(timeout=hard_timeout)
	except subprocess.TimeoutExpired:
		try:
			proc.kill()
		except Exception:
			pass
		try:
			proc.wait(timeout=10)
		except Exception:
			pass
		return {'ok': False, 'path': None, 'error': 'flow hard timeout ' + str(hard_timeout) + 's (worker killed)'}
	try:
		f.close()
	except Exception:
		pass
	if proc.returncode != 0:
		return {'ok': False, 'path': None, 'error': 'flow worker exit ' + str(proc.returncode)}
	if os.path.exists(out_path):
		return {'ok': True, 'path': out_path}
	return {'ok': False, 'path': None, 'error': 'worker exit 0 but no file'}

def create(prompt, out_path, wait=240, aspect=None):
	aspect = aspect or ASPECT
	hard = wait + 120
	return create_with_timeout(prompt, out_path, wait, aspect, hard)


def health():
	try:
		import urllib.request
		urllib.request.urlopen(CDP + '/json/version', timeout=2)
		return {'ok': True}
	except Exception as e:
		return {'ok': False, 'err': str(e)}
