# -- coding: utf-8 --
# modules/render/video.py v4.3.0 - Smart render dispatcher + Engine C overlay + auto CDP
# Engines: flow (Veo) | vids (Google Vids) | ffmpeg (local) | auto
import os, sys, json, time
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
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
	parts = []
	topic = item.get('topic', '') or item.get('title', '')
	if topic:
		parts.append(str(topic))
	for k in ('hook', 'body', 'payoff'):
		v = item.get(k, '')
		if v:
			parts.append(str(v))
	p = ' '.join(parts).strip()
	if not p:
		p = item.get('search_query', '') or 'a short engaging scene'
	tmpl = style.get('ai_prompt_template')
	if tmpl:
		try:
			p = tmpl.format(prompt=p, topic=topic, hook=item.get('hook', ''))
		except Exception:
			pass
	sh = style.get('ai_style')
	if sh:
		p = p + '. ' + str(sh)
	return p[:1500]


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


def try_pexels(prompt, out, wait):
	try:
		from modules.render import pexels_engine as pe
	except Exception as e:
		return {'ok': False, 'error': 'import pexels_engine: ' + str(e)}
	item = {'topic': prompt[:80], 'hook': prompt[:100], 'body': prompt, 'search_query': prompt}
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
	try:
		from ops import ffmpeg_render as fr
	except Exception as e:
		return {'ok': False, 'error': 'import fr: ' + str(e)}
	item = {'topic': prompt[:80], 'hook': prompt[:100], 'body': prompt}
	try:
		r = fr.render_gacha(item, out)
		if os.path.exists(out):
			return {'ok': True, 'path': out, 'engine': 'gacha'}
		return {'ok': False, 'error': 'gacha no output'}
	except Exception as e:
		return {'ok': False, 'error': 'gacha ex: ' + str(e)[:200]}

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
		r = fn(prompt, out, wait)
		res['tried'].append({'engine': eng, 'ok': bool(r.get('ok')), 'error': r.get('error')})
		if r.get('ok') and os.path.exists(out):
			res.update({'ok': True, 'engine': eng, 'path': out})
			return res
		log('engine ' + eng + ' fail: ' + str(r.get('error'))[:160])
	res['error'] = 'all AI engines failed'
	return res


def render(item, out, style=None):
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
	if engine == 'auto':
		use_order = list(FREE_ENGINES)
	elif eo:
		use_order = [e for e in eo if e in ENGINES]
		if engine in ENGINES and engine not in use_order:
			use_order.insert(0, engine)
	r = create(prompt, out, engine=engine, wait=wait, item=item, style=style, order_override=use_order)
	if r.get('ok'):
		log('AI ok engine=' + str(r.get('engine')))
		try:
			record_engine(out, str(r.get('engine')), None, None, True)
		except Exception:
			pass
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
