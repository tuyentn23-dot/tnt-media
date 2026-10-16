# -- coding: utf-8 --
# ops/trend_analyzer.py v3 - Trend theo ngach (YouTube + RSS)
import os, sys, json, time, re, math
import urllib.request
import xml.etree.ElementTree as ET
U2 = chr(95) + chr(95)
FKEY = U2 + 'file' + U2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY])))
sys.path.insert(0, ROOT)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
FEEDS = ['https://trends.google.com/trending/rss?geo=VN']

NICHE_KEYWORDS = {
	'anime': ['anime', 'manga', 'naruto', 'one piece', 'dragon ball', 'pokemon', 'jujutsu', 'demon slayer', 'conan', 'doraemon'],
	'cute_animals': ['meo', 'cho', 'thu cung', 'dong vat', 'pet', 'gau', 'tho', 'chim', 'ca', 'khi', 'voi', 'ho'],
	'meme': ['meme', 'hai huoc', 'viral', 'trend', 'hot', 'gay', 'cuoi'],
	'facts': ['khoa hoc', 'phat minh', 'vu tru', 'trai dat', 'nasa', 'nghien cuu', 'kham pha', 'bi an'],
	'gacha': ['gacha', 'chibi', 'nhan vat', 'game'],
	'roblox': ['roblox', 'minecraft', 'game', 'blocky'],
	'lifestyle': ['song', 'loi song', 'suc khoe', 'dinh duong', 'ngu', 'tap the duc'],
	'nostalgia': ['tuoi tho', 'ky uc', 'ngay xua', 'hoai niem'],
}

NICHE_QUERY = {
	'anime': 'anime edit shorts',
	'cute_animals': 'meo con cute shorts',
	'meme': 'meme hai huoc shorts',
	'facts': 'su that khoa hoc shorts',
	'gacha': 'gacha club shorts',
	'roblox': 'roblox shorts',
	'lifestyle': 'loi song shorts',
	'nostalgia': 'tuoi tho ky uc shorts',
}


def _fetch(url, timeout=15):
	try:
		req = urllib.request.Request(url, headers={'User-Agent': UA})
		r = urllib.request.urlopen(req, timeout=timeout)
		return r.read().decode('utf-8', errors='replace')
	except Exception:
		return ''


def parse_rss(xml_text):
	out = []
	try:
		root = ET.fromstring(xml_text)
	except Exception:
		return out
	for it in root.iter('item'):
		ttl = it.findtext('title') or ''
		lnk = it.findtext('link') or ''
		src = it.findtext('source') or ''
		pub = it.findtext('pubDate') or ''
		if ttl:
			out.append({'title': ttl.strip(), 'link': lnk.strip(), 'source': src.strip(), 'pub': pub.strip()})
	return out


def _age_hours(pub_str):
	if not pub_str:
		return 999
	import email.utils
	try:
		dt = email.utils.parsedate_to_datetime(pub_str)
		return max(0, (time.time() - dt.timestamp()) / 3600.0)
	except Exception:
		return 999


def _niche_match(title, niche=None):
	if not niche or niche not in NICHE_KEYWORDS:
		return 0
	t = str(title).lower()
	n = 0
	for kw in NICHE_KEYWORDS[niche]:
		if kw in t:
			n += 1
	return n


def _youtube_trends(niche, limit=15):
	try:
		from ops.viral_research import youtube as yt
		q = NICHE_QUERY.get(niche) or (niche + ' shorts')
		r = yt.search(q, max_results=limit)
		if not r.get('ok'):
			return []
		items = []
		for it in r.get('items', []):
			v = int(it.get('views') or 0)
			sc = round(math.log10(max(v, 1)) * 2, 2)
			items.append({'title': it.get('title'), 'link': it.get('url'), 'source': 'youtube:' + str(it.get('channel') or '')[:30], 'score': sc, 'views': v, 'duration_s': int(it.get('duration_s') or 0), 'kind': 'video'})
		return items
	except Exception:
		return []


def _score(it, niche=None):
	age = _age_hours(it.get('pub', ''))
	rec = max(0.0, 5.0 - age / 6.0)
	nm = _niche_match(it.get('title', ''), niche) * 3
	ln = len(str(it.get('title', '')))
	len_bonus = 1.0 if 30 <= ln <= 100 else 0.0
	sw = 2.0 if 'trends.google' in str(it.get('link', '')) else 0.5
	return round(rec + nm + len_bonus + sw, 2)


def collect(limit=30, niche=None, kind=None):
	nk = niche or kind
	all_items = []
	if nk:
		all_items.extend(_youtube_trends(nk, limit=limit))
	for url in FEEDS:
		x = _fetch(url)
		if not x:
			continue
		for it in parse_rss(x):
			it['score'] = _score(it, nk)
			all_items.append(it)
	seen = set()
	uniq = []
	for it in all_items:
		k = str(it.get('title', '')).lower()[:60]
		if k in seen:
			continue
		seen.add(k)
		uniq.append(it)
	if nk:
		matched = [x for x in uniq if x.get('kind') == 'video' or _niche_match(x.get('title', ''), nk) > 0]
		if matched:
			uniq = matched
	uniq.sort(key=lambda x: -x.get('score', 0))
	return uniq[:limit]


def save_db(items):
	from pipeline import state
	c = state.connect()
	n = 0
	for it in items:
		try:
			sc = float(it.get('score', 1.0))
			c.execute('INSERT INTO trends (topic, kind, source, score, velocity, ts) VALUES (?,?,?,?,?,?)', (str(it.get('title', ''))[:200], it.get('kind', 'news'), it.get('source', ''), sc, sc, state.now()))
			n += 1
		except Exception:
			pass
	c.commit()
	try:
		c.close()
	except Exception:
		pass
	return n


def run(limit=30, niche=None, kind=None):
	items = collect(limit=limit, niche=niche, kind=kind)
	if not items:
		return {'ok': False, 'error': 'no items'}
	n = save_db(items)
	return {'ok': True, 'collected': len(items), 'saved': n, 'items': items}
