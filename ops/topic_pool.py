# ops/topic_pool.py - pool chu de cu the de chong lap khi sinh noi dung
import random, os, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUSTOM_FILE = os.path.join(ROOT, 'state', 'topic_pool_custom.json')

POOLS = {
	'facts': [
		'Bach tuot co may trai tim?',
		'Ca voi xanh an gi moi ngay?',
		'Loai chim nao bay cao nhat?',
		'Kien co the nang gap may lan trong luong?',
		'Sao Hoa co bao nhieu mat trang?',
		'Cay nao song lau nhat the gioi?',
		'Con vat nao ngu it nhat?',
		'Bao nhieu loai ca map ton tai?',
		'Trai dat nang bao nhieu?',
		'Con nguoi co bao nhieu xuong?',
	],
	'curiosity': [
		'Vi sao bau troi xanh?',
		'Vi sao bien man?',
		'Vi sao meo thich hop?',
		'Vi sao ta ngap?',
		'Vi sao co cau vong?',
	],
	'animals': [
		'Su tu ngu bao nhieu tieng?',
		'Voi co tri nho tot khong?',
		'Ca heo giao tiep the nao?',
		'Chim canh cut giu am the nao?',
		'Ho bao co the chay nhanh bao nhieu?',
	],
	'whatif': [
		'Neu mat troi bien mat thi sao?',
		'Neu trai dat ngung quay thi sao?',
		'Neu con nguoi song 200 nam thi sao?',
		'Neu bien bac cuc tan het thi sao?',
	],
	'cute_animals': [
		'Meo con lam gi khi buon ngu?',
		'Cho con nghi gi ve chu?',
		'Tho con an gi vao buoi sang?',
		'Gau truc con choi gi?',
	],
	'food': [
		'Pho Viet co gi dac biet?',
		'Banh mi Viet khac gi banh mi Phap?',
		'Ca phe sua da bat nguon tu dau?',
	],
	'lifestyle': [
		'3 thoi quen giup ngu ngon hon',
		'Cach giam cang thang trong 5 phut',
		'Vi sao nen di bo moi ngay?',
	],
}

DEFAULT_POOL = [
	'Dieu thu vi ve the gioi tu nhien',
	'Kham pha vu tru rong lon',
	'Bi mat cua dai duong sau tham',
	'Nhung ky quan thien nhien',
]

_seen = {}

def _load_custom():
	try:
		if os.path.exists(CUSTOM_FILE):
			return json.loads(open(CUSTOM_FILE, encoding='utf-8').read())
	except Exception:
		pass
	return {}

def _save_custom(data):
	try:
		os.makedirs(os.path.dirname(CUSTOM_FILE), exist_ok=True)
		json.dump(data, open(CUSTOM_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
		return True
	except Exception:
		return False

def add(kind, topics):
	'''Them nhieu topic vao pool custom. Dedup. Tra ve so topic moi them.'''
	if not kind or not topics:
		return 0
	data = _load_custom()
	cur = data.get(kind) or []
	static = POOLS.get(kind) or []
	existing = set(cur) | set(static)
	added = 0
	for t in topics:
		t = (t or '').strip()
		if t and t not in existing:
			cur.append(t)
			existing.add(t)
			added += 1
	data[kind] = cur
	_save_custom(data)
	return added

def all_topics(kind):
	'''Pool tinh + pool custom cua kind.'''
	static = list(POOLS.get(kind) or [])
	custom = list((_load_custom().get(kind)) or [])
	seen = set()
	out = []
	for t in custom + static:
		if t not in seen:
			seen.add(t)
			out.append(t)
	return out or list(DEFAULT_POOL)

def pick(kind, avoid=None):
	pool = all_topics(kind)
	if avoid:
		pool = [p for p in pool if p not in avoid]
	if not pool:
		pool = all_topics(kind)
	if not pool:
		return None
	seen = _seen.setdefault(kind, set())
	fresh = [p for p in pool if p not in seen]
	if not fresh:
		seen.clear()
		fresh = pool
	choice = random.choice(fresh)
	seen.add(choice)
	return choice

def pool_size(kind):
	return len(all_topics(kind))

def ingest_advisor(payload, kind=None):
	'''Nhan advisor output, map next_ideas -> pool. Tra ve (kind, added).'''
	if not payload or not payload.get('ok'):
		return (None, 0)
	adv = payload.get('advisor') or {}
	ideas = adv.get('next_ideas') or []
	if not ideas:
		return (None, 0)
	if not kind:
		kind = 'curiosity'
	titles = [i.get('title') for i in ideas if isinstance(i, dict) and i.get('title')]
	n = add(kind, titles)
	return (kind, n)
