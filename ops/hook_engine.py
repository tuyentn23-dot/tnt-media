# hook_engine.py - viral hook generation + scoring (flat)
import re, random

PATTERNS = [
 'Ban se khong tin {X} co the lam duoc dieu nay',
 '99% nguoi khong biet su that ve {X}',
 'Dung lam {X} cho toi khi ban xem het video nay',
 'Toi da thu {X} trong 30 ngay va day la ket qua',
 'Su that kinh khung ve {X} ma khong ai noi voi ban',
 '3 dieu ve {X} se thay doi cach ban nghi mai mai',
 'Tai sao {X} lai nguy hiem hon ban tuong',
 'Neu ban thay {X} hay chay ngay',
 'Bi mat {X} duoc giau suot 100 nam',
 '{X} - su that khong the tin noi',
]

HOOK_WORDS = ['khong tin', 'su that', 'bi mat', 'nguy hiem', 'kinh khung', '99%', 'dung lam']

def score(hook):
 h = hook.lower()
 s = 0.0
 s += 25 * sum(1 for w in HOOK_WORDS if w in h)
 s += 20 if any(c.isdigit() for c in hook) else 0
 s += 15 if ('?' in hook or 'tai sao' in h) else 0
 s += 10 if len(hook) <= 60 else -5
 s += 10 if hook[:1].isupper() else 0
 return max(0.0, min(100.0, s))

def generate(topic, n=5, seed=0):
 random.seed(seed or random.randint(0, 99999))
 out = [p.replace('{X}', topic) for p in PATTERNS]
 random.shuffle(out)
 return out[:n]

def best(topic, n=1, seed=0):
 cands = generate(topic, 10, seed)
 ranked = sorted(cands, key=score, reverse=True)
 return ranked[:n]

# Patterns tu TOP video THAT (view cao nhat)
TOP_PATTERNS = [
	'Tai sao {X}? Cau tra loi se khien ban bat ngo',
	'{X} den muc nao? Su that khong ai noi',
	'Bi mat {X} duoc giau suot nhieu nam',
	'Neu {X}, dieu gi se xay ra?',
	'Su that ve {X} ma 99% nguoi khong biet',
]

def top_hooks(topic, name=None):
	n = name or topic
	return [p.replace('{X}', n) for p in TOP_PATTERNS]
