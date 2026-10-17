# ops/ai_content.py - Sinh noi dung moi bang Ollama local
import os, sys, json, time, random, urllib.request, re, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5:7b')
try:
	from ops import vi_query as _vq
except Exception:
	_vq = None
try:
	from ops import topic_pool as _tp
except Exception:
	_tp = None
SESSION_SEEN = {}

KIND_PROMPT = {
	'anime': 'anime, manga, nhan vat anime',
	'roblox': 'game Roblox, nhan vat Roblox',
	'cute_animals': 'dong vat con de thuong, meo, cho, tho',
	'meme': 'tinh huong hai huoc',
	'gacha': 'nhan vat gacha club chibi',
	'facts': 'su that khoa hoc thu vi ve dong vat, tu nhien, vu tru',
	'curiosity': 'dieu thu vi it nguoi biet',
	'whatif': 'gia thuyet khoa hoc',
	'nostalgia': 'ky uc tuoi tho, do vat xua',
	'lifestyle': 'loi song, thoi quen',
	'food': 'mon an ngon',
	'animals': 'the gioi dong vat hoang da',
}

KIND_HINT = {
	'anime': 'hook bat dau bang cau hoi ve nhan vat (VD: Naruto manh nhat khi nao?). Style vui, hype.',
	'roblox': 'hook ve game/update Roblox (VD: Update Roblox moi co gi hot?). Style tre trung.',
	'cute_animals': 'hook ve hanh dong de thuong (VD: Meo con lam gi khi buon ngu?). Style am ap, dang yeu.',
	'meme': 'hook tinh huong hai huoc quen thuoc (VD: Khi ban het tien cuoi thang). Style vui nhe.',
	'gacha': 'hook ve nhan vat gacha (VD: Gacha club co nhan vat nao hot?). Style cute.',
	'facts': 'hook su that bat ngo (VD: Ban co biet bach tuot co 3 trai tim?). Style tom tat.',
	'curiosity': 'hook cau hoi kich thich (VD: Vi sao bau troi xanh?). Style kham pha.',
	'whatif': 'hook gia thuyet hap dan (VD: Neu mat troi bien mat?). Style hoi hop.',
	'nostalgia': 'hook goi ky uc (VD: Ban con nho keo keo nay khong?). Style hoai niem.',
	'lifestyle': 'hook loi song (VD: 3 thoi quen giup ban vui hon). Style huu ich.',
	'food': 'hook mon an (VD: Pho Viet co gi dac biet?). Style ngon mieng.',
	'animals': 'hook dong vat (VD: Su tu ngu bao nhieu tieng 1 ngay?). Style kham pha.',
}



def ensure_ollama():
	'''Kiem tra Ollama, tu start neu chua chay.'''
	import urllib.request, subprocess, os, time, shutil
	try:
		urllib.request.urlopen(OLLAMA_URL + '/api/tags', timeout=2)
		return True
	except Exception:
		pass
	try:
		exe = shutil.which('ollama')
		if not exe:
			return False
		flags = 0x08000000 | 0x00000008
		subprocess.Popen([exe, 'serve'], creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		for _ in range(15):
			time.sleep(2)
			try:
				urllib.request.urlopen(OLLAMA_URL + '/api/tags', timeout=2)
				return True
			except Exception:
				continue
		return False
	except Exception as e:
		print('[ai_content] start err: ', str(e)[:120])
		return False


def _call_ollama(prompt, temperature=0.9, max_tokens=1200, timeout=120, _allow_free=True):
	# Uu tien free LLM (Groq/Gemini) truoc Ollama de nhanh + on dinh
	if _allow_free:
		try:
			from providers import free_llm as _fl0
			if _fl0.available():
				r0 = _fl0.chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens, json_mode=True)
				if r0.get('ok') and (r0.get('text') or '').strip():
					print('[ai_content] free primary:', r0.get('provider'))
					return (r0.get('text') or '').strip()
		except Exception as _fe0:
			print('[ai_content] free primary err:', str(_fe0)[:120])
	if not ensure_ollama():
		print('[ai_content] ollama unavailable')
	try:
		from ops import ollama_boot as _ob
		_ob.ensure()
	except Exception:
		pass
	body = json.dumps({
		'model': OLLAMA_MODEL,
		'prompt': prompt,
		'stream': False,
	'format': 'json',
		'options': {'temperature': 0.7, 'num_predict': max_tokens, 'top_p': 0.9, 'repeat_penalty': 1.1}
	}).encode('utf-8')
	req = urllib.request.Request(OLLAMA_URL + '/api/generate', data=body, headers={'Content-Type': 'application/json'}, method='POST')
	try:
		r = urllib.request.urlopen(req, timeout=timeout)
		d = json.loads(r.read().decode('utf-8'))
		return (d.get('response') or '').strip()
	except Exception as e:
		print('[ai_content] ollama err: ', str(e)[:120])
		if _allow_free:
			try:
				from providers import free_llm as _fl
				r = _fl.chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens, json_mode=True)
				if r.get('ok'):
					print('[ai_content] free fallback:', r.get('provider'))
					return (r.get('text') or '').strip()
			except Exception as _fe:
				print('[ai_content] free fallback err:', str(_fe)[:120])
		return ''


def _clean(s):
	if isinstance(s, list):
		s = ' '.join(str(x) for x in s)
	if not isinstance(s, str):
		s = str(s) if s else ''
	s = s.strip()
	for p in ['1.', '2.', '3.', '- ', '* ']:
		if s.startswith(p):
			s = s[len(p):].strip()
	s = s.strip(chr(34)).strip(chr(39)).strip()
	return s


def _clean_scene(s):
	s = str(s or '').strip()
	s = s.replace(chr(91), '').replace(chr(93), '')
	s = s.replace(chr(34), '').replace(chr(39), '')
	s = s.strip()
	import re as _re
	s = _re.sub('[^a-zA-Z0-9 ,-]+', ' ', s)
	return s.lower().strip()[:80]


def _seen(channel, kind, text):
	k = str(channel) + '|' + str(kind)
	pool = SESSION_SEEN.setdefault(k, set())
	h = hashlib.md5(text.lower().encode()).hexdigest()
	if h in pool:
		return True
	pool.add(h)
	if len(pool) > 500:
		pool.pop()
	return False


def _gen_scenes(hook, body, kind):
	nl = chr(10)
	p1 = 'Sinh mang "scenes" cho video Shorts.'
	p2 = 'Hook: ' + (hook or '')[:100]
	p3 = 'Body: ' + (body or '')[:200]
	p4 = 'Tra ve JSON: {scenes: [4-6 chuoi TIENG ANH, moi chuoi 2-4 tu khoa mo ta hinh anh CU THE cho tung y].}'
	p = p1 + nl + p2 + nl + p3 + nl + p4 + nl + 'CHI tra ve JSON.'
	raw = _call_ollama(p, temperature=0.6, max_tokens=800, timeout=60)
	if not raw:
		return []
	m = re.search(r'{.*}', raw, re.DOTALL)
	if not m:
		return []
	try:
		d = json.loads(m.group(0))
	except Exception:
		return []
	sc = d.get('scenes', [])
	if not isinstance(sc, list):
		return []
	return [_clean_scene(s) for s in sc if s][:6]

def generate_item(channel, kind, attempt=0):
	subj = KIND_PROMPT.get(kind, 'noi dung thu vi')
	hint = KIND_HINT.get(kind, '')
	subj = subj + ((chr(10) + 'Goi y: ' + hint) if hint else '')
	try:
		_tpick = _tp.pick(kind) if _tp else None
	except Exception:
		_tpick = None
	if _tpick:
		subj = _tpick
		hint_extra = 'Chu de CU THE nay: ' + _tpick
		hint = (hint + '. ' + hint_extra) if hint else hint_extra
	is_kids = channel == 'Mialinhcute'
	# Viral research hint (pattern hoc tu video viral)
	viral_hint = ''
	try:
		from ops import viral_research as VR
		cached = VR.latest(1)
		if cached and cached[0].get('summary'):
			s = cached[0]['summary']
			parts = []
			if s.get('pct_question_title', 0) > 30:
				parts.append('dung cau hoi trong hook')
			if s.get('pct_number_title', 0) > 30:
				parts.append('co so lieu trong hook')
			if s.get('pct_emoji_title', 0) > 30:
				parts.append('them emoji')
			if parts:
				viral_hint = 'PATTERN VIRAL: ' + ', '.join(parts)
	except Exception:
		pass
	nl = chr(10)
	req = nl + '=== YEU CAU NGON NGU ==='
	req += nl + 'topic, hook, body, payoff PHAI TIENG VIET CO DAU. search/scenes TIENG ANH.'
	req += nl + '=== TRA VE JSON 1 DONG ==='
	req += nl + 'topic: chu de CU THE, co so lieu/con so. VD: Gau truc co may trai tim? <=55 ky tu.'
	req += nl + 'hook: CAU HOI GAY TO MO + CON SO/SO SANH. VD: Ban co biet trai tim gau truc dap 40 lan/phut? <=95 ky tu.'
	req += nl + 'body: 2-3 cau PHAI co: (1) so lieu that, (2) so sanh/vi von, (3) ly do thu vi. <=240 ky tu.'
	req += nl + 'payoff: cau chot gay bất ngờ hoac cau hoi nguoc. VD: Vay ma chung van ngu 20 tieng/ngay! <=75 ky tu.'
	req += nl + 'search: 3-5 keyword TIENG ANH, CU THE (VD: panda eating bamboo close up).'
	req += nl + 'scenes: mang 4-6 chuoi TIENG ANH, moi chuoi 3-5 tu khoa mo ta HANH DONG CU THE (VD: panda climbing tree slow motion).'
	req += nl + '=== STYLE ==='
	req += nl + 'Hook phai co 1 trong: con so gay shock, so sanh bat ngo, cau hoi nguoc, hoac tiet lo bi mat.'
	req += nl + 'Body tranh tu chung chung (hay, thu vi). Dung dong tu manh + so lieu cu the.'
	req += nl + '=== KHAC BIET ==='
	req += nl + 'Goc nhin doc dao, tranh topic ai cung noi. Long 1 cau chuyen ngan hoac vi du cu the thay vi chi neu su that kho khan.'
	req += nl + 'Neu topic da tung xuat hien (xem danh sach da dang neu co), phai doi sang khia canh MOI hoan toan.'
	if viral_hint:
		req += nl + viral_hint
	if is_kids:
		p = 'Ban la nha sang tao noi dung YouTube Shorts cho TRE EM. Chu de: ' + subj + req + nl + 'VUI VE TICH CUC, KHONG chinh tri, KHONG bao luc.' + nl + 'CHI tra ve 1 dong JSON, KHONG giai thich.'
	else:
		p = 'Ban la nha sang tao noi dung YouTube Shorts. Chu de: ' + subj + req + nl + 'KHONG chinh tri, KHONG bao luc.' + nl + 'CHI tra ve 1 dong JSON, KHONG giai thich.'
	raw = _call_ollama(p, temperature=0.85 + attempt * 0.05, max_tokens=1500)
	if not raw:
		return None
	m = re.search(r'{.*}', raw, re.DOTALL)
	if not m:
		return None
	try:
		d = json.loads(m.group(0))
	except Exception:
		return None
	topic = _clean(d.get('topic', ''))
	hook = _clean(d.get('hook', ''))
	body = _clean(d.get('body', ''))
	payoff = _clean(d.get('payoff', ''))
	search = _clean(d.get('search', ''))
	scenes = d.get('scenes', [])
	if not topic or not hook:
		return None
	if _seen(channel, kind, topic):
		return None
	try:
		from modules.render import vn_guard as _vg
		# Thu 1: guard truc tiep
		_guard_ok = True
		for _t in (topic, hook, body, payoff):
			if not _vg.check(_t).get('ok'):
				_guard_ok = False
				break
		# Thu 2: neu thieu dau -> phuc hoi dau roi kiem lai
		if not _guard_ok:
			try:
				from ops import voice_script as _vs
				_fix = lambda _x: _x if _vs.has_diacritics(_x) else _vs.restore_diacritics(_x)
				topic, hook, body, payoff = _fix(topic), _fix(hook), _fix(body), _fix(payoff)
				_guard_ok = all(_vg.check(_t).get('ok') for _t in (topic, hook, body, payoff))
				print('[ai_content] diacritic recovered: '+str(_guard_ok))
			except Exception as _de:
				print('[ai_content] diacritic fix err: '+str(_de)[:80])
		if not _guard_ok:
			print('[ai_content] reject no-diacritic: '+str(topic)[:60].encode('ascii','replace').decode('ascii'))
			return None
	except Exception as _e:
		print('[ai_content] vn_guard err: '+str(_e)[:80].encode('ascii','replace').decode('ascii'))
	iid = 'ai_' + kind + '_' + hashlib.md5(topic.encode()).hexdigest()[:10]
	return {
		'id': iid,
		'topic': topic,
		'hook': hook,
		'body': body or hook,
		'payoff': payoff or topic,
		'search_query': _vq.to_en_query(search, topic, kind),
		'scenes': ([_clean_scene(s) for s in scenes if s][:6] if isinstance(scenes, list) and scenes else _gen_scenes(hook, body, kind)),
		'kind': kind,
		'source': 'ai',
	}


def generate(channel, kind, limit=5):
	out = []
	max_attempts = max(limit * 3, 8)
	att = 0
	while len(out) < limit and att < max_attempts:
		it = generate_item(channel, kind, attempt=att % 3)
		if it:
			out.append(it)
		att += 1
	if not out:
		out.append(_fallback_item(kind))
	return out

def _fallback_item(kind):
	import time as _t
	pool = [
		('Bạn có biết loài vật nào ngủ ít nhất không?', 'Loài vật ngủ ít nhất là hươu cao cổ, chỉ khoảng 2 tiếng mỗi ngày.', 'Hãy theo dõi để khám phá thêm!'),
		('Bạn có biết trái tim cá voi lớn cỡ nào không?', 'Trái tim cá voi xanh có thể nặng tới 180 kg, lớn như một chiếc xe hơi nhỏ.', 'Thiên nhiên thật kỳ diệu!'),
		('Bạn có biết loài chim nào bay cao nhất không?', 'Kền kền Rüppell có thể bay cao tới 11.000 mét, cao hơn đỉnh Everest.', 'Khám phá thêm nhiều điều thú vị nhé!'),
	]
	i = int(t.time()) % len(pool)
	hook, body, payoff = pool[i]
	topic = hook
	iid = 'ai_fb' + str(int(_t.time()))
	return {
		'id': iid,
		'topic': topic,
		'hook': hook,
		'body': body,
		'payoff': payoff,
		'search_query': 'amazing animal facts',
		'scenes': ['amazing animals wild', 'nature documentary', 'wildlife close-up'],
		'kind': kind,
		'source': 'ai_fallback',
	}





def warmup():
	try:
		return _call_ollama('hi', max_tokens=5, timeout=30)
	except Exception:
		return ''

def health():
	try:
		r = urllib.request.urlopen(OLLAMA_URL + '/api/tags', timeout=3)
		d = json.loads(r.read().decode('utf-8'))
		return {'ok': True, 'model': OLLAMA_MODEL, 'available': [m.get('name') for m in d.get('models', [])]}
	except Exception as e:
		return {'ok': False, 'error': str(e)[:120]}

