# ops/ai_content.py - Sinh noi dung moi bang Ollama local
import os, sys, json, time, random, urllib.request, re, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5:7b')
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


def _call_ollama(prompt, temperature=0.9, max_tokens=400, timeout=120):
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
		'options': {'temperature': temperature, 'num_predict': max_tokens, 'top_p': 0.95}
	}).encode('utf-8')
	req = urllib.request.Request(OLLAMA_URL + '/api/generate', data=body, headers={'Content-Type': 'application/json'}, method='POST')
	try:
		r = urllib.request.urlopen(req, timeout=timeout)
		d = json.loads(r.read().decode('utf-8'))
		return (d.get('response') or '').strip()
	except Exception as e:
		print('[ai_content] err: ', str(e)[:120])
		return ''


def _clean(s):
	s = (s or '').strip()
	for p in ['1.', '2.', '3.', '- ', '* ']:
		if s.startswith(p):
			s = s[len(p):].strip()
	s = s.strip(chr(34)).strip(chr(39)).strip()
	return s


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


def generate_item(channel, kind, attempt=0):
	subj = KIND_PROMPT.get(kind, 'noi dung thu vi')
	hint = KIND_HINT.get(kind, '')
	subj = subj + ((chr(10) + 'Goi y: ' + hint) if hint else '')
	is_kids = channel == 'Mialinhcute'
	nl = chr(10)
	req = nl + 'QUAN TRONG: Tra loi HOAN TOAN bang TIENG VIET (khong dung tieng Anh).'
	req += nl + 'Tra ve JSON 1 dong voi cac truong: topic, hook, body, payoff, search.'
	req += nl + 'topic: CHU DE CU THE (VD: Gau truc co may trai tim?). Khong ghi chung chung. <=60 ky tu.'
	req += nl + 'hook: cau hoi hap dan (<=100 ky tu).'
	req += nl + 'body: 2-3 cau thong tin CU THE tra loi hook (<=250 ky tu).'
	req += nl + 'payoff: cau ket (<=80 ky tu).'
	req += nl + 'search: 3-5 tu khoa TIENG ANH de tim video stock (VD: cute cat playing).'
	if is_kids:
		p = 'Ban la nha sang tao noi dung YouTube Shorts cho TRE EM. Chu de: ' + subj + req + nl + 'VUI VE TICH CUC, KHONG chinh tri, KHONG bao luc.' + nl + 'CHI tra ve 1 dong JSON, KHONG giai thich.'
	else:
		p = 'Ban la nha sang tao noi dung YouTube Shorts. Chu de: ' + subj + req + nl + 'KHONG chinh tri, KHONG bao luc.' + nl + 'CHI tra ve 1 dong JSON, KHONG giai thich.'
	raw = _call_ollama(p, temperature=0.85 + attempt * 0.05)
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
	if not topic or not hook:
		return None
	if _seen(channel, kind, topic):
		return None
	iid = 'ai_' + kind + '_' + hashlib.md5(topic.encode()).hexdigest()[:10]
	return {
		'id': iid,
		'topic': topic,
		'hook': hook,
		'body': body or hook,
		'payoff': payoff or topic,
		'search_query': search or topic,
		'kind': kind,
		'source': 'ai',
	}


def generate(channel, kind, limit=5):
	out = []
	max_attempts = limit * 4
	att = 0
	while len(out) < limit and att < max_attempts:
		it = generate_item(channel, kind, attempt=att % 3)
		if it:
			out.append(it)
		att += 1
	return out




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

