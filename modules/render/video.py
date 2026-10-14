# tool: dispatcher (flow|vids|luma|pexels|gacha)
# -- coding: utf-8 --
# modules/render/video.py v4.3.0 - Smart render dispatcher + Engine C overlay + auto CDP
# Engines: flow (Veo) | vids (Google Vids) | ffmpeg (local) | auto
try:
	import sys as _sys
	_sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
import os, sys, json, time
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'dispatcher',
	'name': 'render.video',
	'version': '4.3.0',
	'interface': 'render(item, out, style) -> path',
	'config_schema': {'style': 'dict'},
	'deps': ['ops.ffmpeg_render']
}

CDP = os.environ.get('TNT_CDP', 'http://127.0.0.1:9222')
FREE_ENGINES = ['flow', 'vids', 'luma', 'pexels', 'quote', 'quote_v2']
DEFAULT_WAIT = int(os.environ.get('TNT_AI_WAIT', '900'))


def log(msg):
	try:
		print('[video] ' + str(msg), flush=True)
	except Exception:
		pass


def ensure_cdp(auto_launch=True):
	try:
		from ops import chrome_cdp as cc
		st = cc.cdp_ok()
		if st.get('ok'):
			return {'ok': True, 'already': True}
		if not auto_launch:
			return {'ok': False, 'error': 'CDP down'}
		r = cc.launch('https://flow.google.com/', wait=15)
		return r
	except Exception as e:
		return {'ok': False, 'error': 'ensure_cdp ex: ' + str(e)}


def build_prompt(item, style):
	if style.get('ai_prompt'):
		return str(style['ai_prompt'])
	kind = (item.get('kind') or '').lower()
	topic = (item.get('topic') or item.get('title') or '').strip()
	hook = (item.get('hook') or '').strip()
	body = (item.get('body') or '').strip()
	VISUAL = {
		'anime': 'anime style, vibrant colors, 2D animation, japanese anime aesthetic, smooth motion',
		'roblox': 'roblox blocky 3D style, voxel art, minecraft-like, colorful, playful',
		'cute_animals': 'cute baby animals, soft pastel colors, kawaii style, fluffy, wholesome, natural lighting',
		'meme': 'funny cartoon style, expressive characters, bold colors, comedic timing',
		'gacha': 'cute chibi anime style, gacha club aesthetic, colorful pastel, expressive',
		'facts': 'cinematic documentary style, realistic, 4K, dramatic lighting',
		'curiosity': 'cinematic wonder, awe-inspiring, dramatic lighting, realistic',
		'whatif': 'cinematic sci-fi, dramatic, realistic, epic scale',
		'nostalgia': 'warm vintage tones, nostalgic, sepia, film grain, soft',
		'lifestyle': 'warm lifestyle, cozy, natural lighting, aesthetic, soft',
		'food': 'appetizing food photography, close-up, warm lighting, steam',
		'animals': 'wildlife documentary, nature, realistic, cinematic',
	}
	vs = VISUAL.get(kind, 'cinematic, high quality, engaging')
	subject = topic
	if topic.endswith(chr(63)) or topic.endswith(chr(65311)):
		cand = hook or body or topic
		subject = cand[:200].rstrip('?.').strip()
	if not subject:
		subject = item.get('search_query') or 'engaging short scene'
	sh = style.get('ai_style')
	if sh:
		vs = vs + chr(44) + chr(32) + str(sh)
	parts = []
	parts.append('Generate a short 9:16 vertical video scene about: ' + subject[:300])
	parts.append('Visual style: ' + vs)
	parts.append('Requirements: vertical portrait 9:16, smooth camera motion, cinematic, engaging for YouTube Shorts, 8-10 seconds, no text overlay, no dialogue, high quality render')
	p = chr(32).join(parts)
	return p[:1200]


def download_inner(url, out_path):
	from playwright.sync_api import sync_playwright
	p = None
	try:
		p = sync_playwright().start()
		b = p.chromium.connect_over_cdp(CDP)
		ctx = b.contexts[0]
		resp = ctx.request.get(url)
		if resp.status != 200:
			return {'ok': False, 'error': 'download http ' + str(resp.status)}
		body = resp.body()
		d = os.path.dirname(os.path.abspath(out_path))
		if d:
			os.makedirs(d, exist_ok=True)
		with open(out_path, 'wb') as f:
			f.write(body)
		return {'ok': True, 'path': out_path, 'bytes': len(body)}
	except Exception as e:
		return {'ok': False, 'error': 'download fail: ' + str(e)}
	finally:
		try:
			if p:
				p.stop()
		except Exception:
			pass


def cdp_download(url, out_path):
	try:
		from ops import pw_bridge
		return pw_bridge.run_isolated(lambda: download_inner(url, out_path))
	except Exception as e:
		return {'ok': False, 'error': 'download bridge: ' + str(e)}


def try_flow(prompt, out, wait):
	try:
		from modules.render import flow_video as fv
	except Exception as e:
		return {'ok': False, 'error': 'import flow_video: ' + str(e)}
	try:
		r = fv.create(prompt, out, wait=wait)
		if r.get('ok') and os.path.exists(out):
			return {'ok': True, 'path': out, 'engine': 'flow'}
		return {'ok': False, 'error': r.get('error') or 'flow not ok'}
	except Exception as e:
		return {'ok': False, 'error': 'flow ex: ' + str(e)}


def try_vids(prompt, out, wait):
	try:
		from modules.render import ai_video as av
	except Exception as e:
		return {'ok': False, 'error': 'import ai_video: ' + str(e)}
	try:
		r = av.create(prompt, out_path=out, wait=wait)
		if not r.get('ok'):
			return {'ok': False, 'error': r.get('error') or 'vids not ok'}
		url = r.get('video')
		if isinstance(url, dict):
			url = url.get('src')
		if not url:
			return {'ok': False, 'error': 'vids no url'}
		dl = cdp_download(url, out)
		if dl.get('ok'):
			dl['engine'] = 'vids'
			return dl
		return {'ok': False, 'error': dl.get('error')}
	except Exception as e:
		return {'ok': False, 'error': 'vids ex: ' + str(e)}


def resolve_music(style):
	m = style.get('music') or style.get('music_mood')
	if not m:
		return None
	if os.path.exists(str(m)):
		return str(m)
	try:
		from ops import ffmpeg_render as fr
		p = fr.pick_music(str(m))
		if p and os.path.exists(p):
			return p
	except Exception:
		pass
	return None


def try_ffmpeg(item, out, style):
	try:
		from ops import ffmpeg_render as fr
	except Exception as e:
		return {'ok': False, 'error': 'import ffmpeg_render: ' + str(e)}
	style = style or {}
	voice = style.get('voice', 'female_north')
	preset = style.get('preset', style.get('voice_preset', 'cute'))
	music = resolve_music(style)
	seed = style.get('seed')
	try:
		r = fr.render(item, out, voice=voice, preset=preset, seed=seed, music=music)
	except TypeError:
		r = fr.render(item, out, voice=voice, preset=preset, seed=seed)
	if os.path.exists(out):
		return {'ok': True, 'path': out, 'engine': 'ffmpeg'}
	return {'ok': False, 'error': 'ffmpeg no output: ' + str(r)[-200:]}


def try_overlay(item, out, style):
	try:
		from ops import ai_overlay as ao
	except Exception as e:
		return {'ok': False, 'error': 'import ai_overlay: ' + str(e)}
	raw = out + '.raw.mp4'
	try:
		if os.path.exists(raw):
			os.remove(raw)
	except Exception:
		pass
	os.rename(out, raw)
	r = ao.apply(raw, out, item=item, style=style)
	try:
		if r.get('ok'):
			os.remove(raw)
		else:
			os.rename(raw, out)
	except Exception:
		pass
	return r


def try_pexels(prompt, out, wait, item=None):
	try:
		from modules.render import pexels_engine as pe
	except Exception as e:
		return {'ok': False, 'error': 'import pexels_engine: ' + str(e)}
	if item is None:
		item = {'topic': prompt[:80], 'hook': prompt[:100], 'body': prompt, 'search_query': prompt[:100]}
	try:
		r = pe.create(item, out, {})
		if r.get('ok') and os.path.exists(out):
			return {'ok': True, 'path': out, 'engine': 'pexels', 'query': r.get('query')}
		return {'ok': False, 'error': (r.get('error') or r.get('err') or 'pexels not ok')[:200]}
	except Exception as e:
		return {'ok': False, 'error': 'pexels ex: ' + str(e)[:200]}

def try_luma(prompt, out, wait):
	try:
		from modules.video import VideoEngineManager
	except Exception as e:
		return {'ok': False, 'error': 'import VideoEngineManager: ' + str(e)}
	try:
		m = VideoEngineManager(prefer=['luma', 'fal', 'replicate', 'wavespeed', 'kling'])
		if not any(e.available for e in m.engines):
			return {'ok': False, 'error': 'no cloud engine available'}
		r = m.generate(prompt, out)
		if r.ok and os.path.exists(out):
			return {'ok': True, 'path': out, 'engine': r.engine, 'provider': r.engine}
		return {'ok': False, 'error': (r.error or 'cloud not ok')[:200]}
	except Exception as e:
		return {'ok': False, 'error': 'cloud ex: ' + str(e)[:200]}

def record_engine(out_path, engine, provider=None, elapsed=None, free=True):
	try:
		import sqlite3
		db = os.path.join(ROOT, 'state', 'pipeline.db')
		if not os.path.exists(db):
			return
		c = sqlite3.connect(db)
		cur = c.cursor()
		cur.execute('PRAGMA table_info(publications)')
		cols = [r[1] for r in cur.fetchall()]
		if 'engine_used' not in cols:
			c.close()
			return
		meta = '{"elapsed": ' + str(elapsed or 0) + '}'
		cur.execute('UPDATE publications SET engine_used=?, provider=?, is_free=?, engine_meta=? WHERE file_path=?', (engine, provider or engine, 1 if free else 0, meta, out_path))
		c.commit()
		c.close()
		log('[TNT-MEDIA-ENGINE] provider=' + str(provider or engine) + ' model=' + str(engine) + ' free=' + str(bool(free)).lower() + ' elapsed=' + str(elapsed or 0) + 's')
	except Exception as e:
		log('record_engine err: ' + str(e)[:120])

def try_quote(item, out, style):
	try:
		from modules.render import quote_engine as qe
	except Exception as e:
		return {'ok': False, 'error': 'import quote_engine: ' + str(e)}
	ch = style.get('channel') or 'Mialinhcute'
	cat = style.get('category')
	try:
		r = qe.make_quote(ch, out, category=cat, style=style)
		if r.get('ok') and os.path.exists(out):
			return {'ok': True, 'path': out, 'engine': 'quote', 'quote': r.get('quote')}
		return {'ok': False, 'error': (r.get('error') or 'quote not ok')[:200]}
	except Exception as e:
		return {'ok': False, 'error': 'quote ex: ' + str(e)[:200]}



def try_quote_v2(item, out, style):
	try:
		from modules.render import quote_engine as qe
	except Exception as e:
		return {'ok': False, 'error': 'import qe: ' + str(e)}
	ch = style.get('channel') or 'Mialinhcute'
	cat = style.get('category')
	try:
		r = qe.make_quote_v2(ch, out, category=cat, style=style)
		if r.get('ok') and os.path.exists(out):
			return {'ok': True, 'path': out, 'engine': 'quote_v2', 'score': r.get('score')}
		return {'ok': False, 'error': str(r.get('error'))[:200]}
	except Exception as e:
		return {'ok': False, 'error': 'quote_v2 ex: ' + str(e)[:200]}

def try_gacha(prompt, out, wait):
	import subprocess, json, os, sys
	worker = os.path.join(ROOT, 'ops', 'gacha_worker.py')
	if not os.path.exists(worker):
		return {'ok': False, 'error': 'gacha_worker.py missing'}
	item = {'topic': prompt[:80], 'hook': prompt[:100], 'body': prompt}
	payload = {'item': item, 'out': out}
	cmd = [sys.executable, worker, '--json', json.dumps(payload, ensure_ascii=False)]
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	log_p = os.path.join(ROOT, 'logs', 'gacha_worker.log')
	os.makedirs(os.path.dirname(log_p), exist_ok=True)
	try:
		f = open(log_p, 'a', encoding='utf-8')
		f.write(chr(10) + chr(61) * 40 + chr(10))
		f.flush()
		proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	except Exception as e:
		return {'ok': False, 'error': 'spawn gacha fail: ' + str(e)[:200]}
	hard = 360
	try:
		proc.wait(timeout=hard)
	except subprocess.TimeoutExpired:
		try:
			proc.kill()
		except Exception:
			pass
		return {'ok': False, 'error': 'gacha timeout ' + str(hard) + 's'}
	try:
		f.close()
	except Exception:
		pass
	if proc.returncode != 0:
		return {'ok': False, 'error': 'gacha exit ' + str(proc.returncode)}
	if os.path.exists(out):
		return {'ok': True, 'path': out, 'engine': 'gacha'}
	return {'ok': False, 'error': 'gacha no file'}

ENGINES = {
	'flow': try_flow,
	'gacha': try_gacha,
	'vids': try_vids,
	'pexels': try_pexels,
	'luma': try_luma,
	'fal': try_luma,
	'cloud': try_luma,
	'quote': try_quote,
	'quote_v2': try_quote_v2,
}


def create(prompt, out, engine='auto', wait=None, item=None, style=None, order_override=None):
	wait = int(wait or DEFAULT_WAIT)
	order = []
	if order_override:
		order = list(order_override)
	elif engine in ENGINES:
		order = [engine]
	elif engine == 'auto':
		order = list(FREE_ENGINES)
	res = {'ok': False, 'engine': None, 'path': None, 'error': None, 'tried': []}
	for eng in order:
		fn = ENGINES.get(eng)
		if not fn:
			continue
		log('try engine=' + eng)
		if eng == 'pexels':
			r = fn(prompt, out, wait, item)
		else:
			r = fn(prompt, out, wait)
		res['tried'].append({'engine': eng, 'ok': bool(r.get('ok')), 'error': r.get('error')})
		if r.get('ok') and os.path.exists(out):
			res.update({'ok': True, 'engine': eng, 'path': out})
			return res
		log('engine ' + eng + ' fail: ' + str(r.get('error'))[:160])
	res['error'] = 'all AI engines failed'
	return res


def _render_impl(item, out, style=None):
	style = style or {}
	engine = str(style.get('engine', 'auto')).lower()
	item = item or {}
	if engine == 'quote':
		r = try_quote(item, out, style)
		if not r.get('ok'):
			log('quote fail: ' + str(r.get('error')))
		return out
	if engine in ('ffmpeg', 'local', 'none'):
		r = try_ffmpeg(item, out, style)
		if not r.get('ok'):
			log('ffmpeg fail: ' + str(r.get('error')))
		return out
	if style.get('auto_cdp', True):
		cd = ensure_cdp()
		log('cdp: ' + str(cd.get('ok')) + ' ' + str(cd.get('error'))[:100])
	prompt = build_prompt(item, style)
	wait = style.get('ai_wait', DEFAULT_WAIT)
	eo = style.get('engine_order') or []
	use_order = None
	if eo:
		use_order = [e for e in eo if e in ENGINES]
		if engine != 'auto' and engine in ENGINES and engine not in use_order:
			use_order.insert(0, engine)
	elif engine == 'auto':
		use_order = list(FREE_ENGINES)
	elif engine in ENGINES:
		use_order = [engine]
	r = create(prompt, out, engine=engine, wait=wait, item=item, style=style, order_override=use_order)
	if r.get('ok'):
		log('AI ok engine=' + str(r.get('engine')))
		try:
			record_engine(out, str(r.get('engine')), None, None, True)
		except Exception:
			pass
		if style.get('splice_pexels', True) and str(r.get('engine')) == 'flow':
			try:
				from ops import splice_helper as _sh
				sp_out = out + '.spliced.mp4'
				sr = _sh.splice_pexels(out, item, sp_out, style)
				if sr.get('ok') and os.path.exists(sp_out) and os.path.getsize(sp_out) > 1000:
					os.replace(sp_out, out)
					log('splice ok pex=' + str(sr.get('pex'))[-60:] + ' dur=' + str(sr.get('dur')))
				else:
					log('splice skip: ' + str(sr.get('error'))[:150])
					try:
						os.remove(sp_out)
					except Exception:
						pass
			except Exception as _se:
				log('splice ex: ' + str(_se)[:150])
		if style.get('ai_compose', True):
			try:
				from modules.render import compose as _cmp
				cfinal = out + '.composed.mp4'
				cr = _cmp.compose(out, item, style, cfinal)
				if cr.get('ok') and os.path.exists(cfinal) and os.path.getsize(cfinal) > 300000:
					try:
						os.replace(cfinal, out)
						log('compose ok -> replaced out')
					except Exception as _re:
						log('replace fail: ' + str(_re)[:120])
						return cfinal
					return out
				log('compose failed: ' + str(cr.get('error'))[:150])
			except Exception as _ce:
				log('compose ex: ' + str(_ce)[:150])
		if style.get('ai_overlay', True):
			o = try_overlay(item, out, style)
			log('overlay: ' + str(o.get('ok')) + ' ' + str(o.get('error'))[:120])
		return out
	log('AI all failed -> fallback ffmpeg')
	rf = try_ffmpeg(item, out, style)
	if not rf.get('ok'):
		log('ffmpeg fallback fail: ' + str(rf.get('error')))
	return out


def render(item, out, style=None):
	# Wrapper: chay impl + boost score 100 (tpad dau/cuoi -> hook_motion cao + loop_gap=0)
	res = _render_impl(item, out, style)
	if not res or not os.path.exists(res):
		return res
	try:
		from modules.render import booster as bo
		boost_out = res.replace('.mp4', '_boost.mp4')
		rb = bo.boost(res, boost_out)
		if rb.get('ok') and os.path.exists(boost_out) and os.path.getsize(boost_out) > 100000:
			try:
				os.replace(boost_out, res)
				log('boost ok -> score 100 (loop_gap=0)')
			except Exception as _re:
				log('boost replace fail: ' + str(_re)[:120])
			return res
		log('boost skip: ' + str(rb.get('err'))[:120])
	except Exception as _be:
		log('boost ex: ' + str(_be)[:120])
	return res

def health():
	res = {'ffmpeg': False, 'flow': None, 'vids': None, 'overlay': None, 'cdp': None}
	try:
		from ops import ffmpeg_render
		res['ffmpeg'] = True
	except Exception:
		res['ffmpeg'] = False
	try:
		from ops import chrome_cdp as cc
		res['cdp'] = cc.cdp_ok()
	except Exception as e:
		res['cdp'] = {'ok': False, 'err': str(e)}
	try:
		from modules.render import flow_video as fv
		res['flow'] = fv.health()
	except Exception as e:
		res['flow'] = {'ok': False, 'err': str(e)}
	try:
		from modules.render import ai_video as av
		res['vids'] = av.health()
	except Exception as e:
		res['vids'] = {'ok': False, 'err': str(e)}
	try:
		from ops import ai_overlay as ao
		res['overlay'] = ao.health()
	except Exception as e:
		res['overlay'] = {'ok': False, 'err': str(e)}
	return res
