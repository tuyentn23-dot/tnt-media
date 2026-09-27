# crawler v2
import os, sys, json, time, html
import urllib.request, urllib.parse
import xml.etree.ElementTree as ET
ROOT = os.getcwd()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

def fetch(url, timeout=15):
	try:
		req = urllib.request.Request(url, headers={'User-Agent': UA})
		r = urllib.request.urlopen(req, timeout=timeout)
		return r.read().decode('utf-8', errors='replace')
	except Exception:
		return ''

def clean(s):
	s = html.unescape(s or '')
	return ' '.join(s.split())

RSS = [
	{'url': 'https://vnexpress.net/rss/tin-moi-nhat.rss', 'cat': 'news', 'lang': 'vi'},
	{'url': 'https://vnexpress.net/rss/the-gioi.rss', 'cat': 'world', 'lang': 'vi'},
	{'url': 'https://vnexpress.net/rss/giai-tri.rss', 'cat': 'ent', 'lang': 'vi'},
	{'url': 'https://vnexpress.net/rss/khoa-hoc.rss', 'cat': 'sci', 'lang': 'vi'},
	{'url': 'https://vnexpress.net/rss/suc-khoe.rss', 'cat': 'health', 'lang': 'vi'},
	{'url': 'https://vnexpress.net/rss/giao-duc.rss', 'cat': 'edu', 'lang': 'vi'},
	{'url': 'https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi', 'cat': 'hot', 'lang': 'vi'},
	{'url': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en', 'cat': 'world', 'lang': 'en'},
]

def parse_rss(xml, src):
	out = []
	try:
		root = ET.fromstring(xml)
	except Exception:
		return out
	for it in root.iter('item'):
		ttl = clean((it.findtext('title') or ''))[:200]
		dsc = clean((it.findtext('description') or ''))[:500]
		lnk = (it.findtext('link') or '')[:300]
		if not ttl: continue
		out.append({'title': ttl, 'body': dsc, 'url': lnk, 'cat': src['cat'], 'lang': src['lang']})
	return out

def crawl_rss():
	out = []
	for s in RSS:
		xml = fetch(s['url'])
		if not xml: continue
		out.extend(parse_rss(xml, s))
	return out

def wiki_random(lang='vi', limit=10):
	url = 'https://' + lang + '.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=' + str(limit) + '&format=json'
	txt = fetch(url)
	if not txt: return []
	try:
		j = json.loads(txt)
		return [{'title': x['title'], 'lang': lang} for x in j.get('query', {}).get('random', [])]
	except Exception:
		return []

def wiki_summary(title, lang='vi'):
	url = 'https://' + lang + '.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(title)
	txt = fetch(url)
	if not txt: return None
	try:
		return json.loads(txt)
	except Exception:
		return None
