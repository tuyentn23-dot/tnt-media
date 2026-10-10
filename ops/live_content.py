# -- coding: utf-8 --
import os, sys, hashlib
sys.path.insert(0, os.getcwd())
from ops import content_crawler as cc

KIND_MAP = {
	'news': ['news', 'hot'],
	'world': ['world'],
	'facts': ['sci', 'health', 'edu', 'world'],
	'sci': ['sci', 'health'],
	'ent': ['ent', 'hot'],
	'lifestyle': ['health', 'edu', 'news'],
	'food': ['health', 'news'],
	'animals': ['sci', 'world'],
	'curiosity': ['sci', 'hot'],
	'whatif': ['sci', 'world'],
	'nostalgia': ['news', 'ent'],
	'anime': ['ent', 'hot'],
	'roblox': ['ent', 'hot'],
	'cute_animals': ['sci', 'world'],
	'meme': ['ent', 'hot'],
	'gacha': ['ent', 'hot'],
}

CHANNEL_NICHE = {
	'Mialinhcute': 'kids',
	'vilevi5676': 'general',
	'MinhTriet-AI': 'general',
}

FORBIDDEN_KW = ['hiếp dâm', 'cưỡng hiếp', 'tự tử', 'giết người', 'ma túy', 'đâm nhau']

KIDS_FORBIDDEN = ['thủ tướng', 'tổng thống', 'chính phủ', 'bầu cử', 'quốc hội', 'bom', 'chiến tranh', 'xung đột', 'israel', 'ukraine', 'nga', 'biểu tình', 'tai nạn', 'tử vong', 'thiệt mạng', 'netanyahu', 'putin', 'trump', 'zelensky', 'ca sĩ', 'nghệ sĩ', 'tom cruise', 'hollywood', 'showbiz', 'ly hôn', 'kết hôn', 'tình ái', 'scandal', 'ma túy', 'tù', 'phạm', 'tội', 'u ám', 'kinh dị', 'chiến sự', 'quân sự', 'tên lửa', 'chết']


def _slug(s):
	return hashlib.sha1((s or '').encode()).hexdigest()[:10]


def _strip_html(s):
	from html.parser import HTMLParser
	class P(HTMLParser):
		def __init__(self):
			super().__init__()
			self.parts = []
		def handle_data(self, d):
			self.parts.append(d)
	pp = P()
	try:
		pp.feed(s or '')
	except Exception:
		return (s or '').strip()
	import re
	txt = ' '.join(pp.parts)
	txt = re.sub(r'https?://\S+', '', txt)
	txt = re.sub(r'\s+', ' ', txt)
	return txt.strip()


def is_forbidden(text):
	low = (text or '').lower()
	for k in FORBIDDEN_KW:
		if k.lower() in low:
			return True
	return False


def is_kids_unsafe(text):
	low = (text or '').lower()
	for k in KIDS_FORBIDDEN:
		if k.lower() in low:
			return True
	return False


def rss_to_item(r, kind, channel):
	title = _strip_html(r.get('title') or '')
	body = _strip_html(r.get('body') or '')
	url = r.get('url', '')
	if len(title) < 20:
		return None
	vid = 'live_' + kind + '_' + _slug(title + url)
	hook = title[:150]
	b = body[:600] if body else title
	payoff = title[:80]
	return {'id': vid, 'topic': title[:120], 'kind': kind, 'hook': hook, 'body': b, 'payoff': payoff, 'source_url': url}


def generate(channel, kind, limit=30):
	cats = KIND_MAP.get(kind, ['news'])
	try:
		items = cc.crawl_rss()
	except Exception as e:
		print('[live] err:', str(e)[:80])
		items = []
	filtered = [r for r in items if r.get('cat') in cats]
	out = []
	seen = set()
	for r in filtered:
		it = rss_to_item(r, kind, channel)
		if not it:
			continue
		if it['id'] in seen:
			continue
		seen.add(it['id'])
		out.append(it)
		if len(out) >= limit:
			break
	return out


def filter_items(items, channel_id=None):
	out = []
	is_kids_ch = bool(channel_id and CHANNEL_NICHE.get(channel_id) == 'kids')
	for it in items:
		txt = str(it.get('hook')) + ' ' + str(it.get('body'))
		if is_forbidden(txt):
			continue
		if is_kids_ch and is_kids_unsafe(txt):
			continue
		out.append(it)
	return out


if __name__ == '__main__':
	items = generate('vilevi5676', 'news', 5)
	print('Generated:', len(items))
	for it in items[:5]:
		print(' -', it['id'], it['hook'][:80])
