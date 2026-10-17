# ops/studio_advisor.py - Ask Studio noi bo: phan tich kenh + goi y noi dung bang Ollama
import os, sys, json, time, pickle
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
CACHE = os.path.join(ROOT, 'state', 'studio_advisor_cache.json')
TOKEN_DEFAULT = os.path.join(ROOT, 'config', 'token.pickle')

def _token_path(channel_id=None):
	if channel_id:
		try:
			from ops import channel_loader as _ch
			cfg = _ch.load(channel_id)
			tp = _ch.token_path(cfg)
			if tp and os.path.exists(tp):
				return tp
		except Exception:
			pass
	if os.path.exists(TOKEN_DEFAULT):
		return TOKEN_DEFAULT
	p2 = os.path.join(ROOT, 'token.pickle')
	return p2 if os.path.exists(p2) else None

def _yt(channel_id=None):
	from googleapiclient.discovery import build
	tp = _token_path(channel_id)
	if not tp:
		return None
	f = open(tp, 'rb')
	creds = pickle.load(f)
	f.close()
	return build('youtube', 'v3', credentials=creds)

def fetch_channel_snapshot(channel_id=None):
	yt = _yt(channel_id)
	if not yt:
		return {'ok': False, 'error': 'no token'}
	r = yt.channels().list(part='snippet,statistics,contentDetails', mine=True).execute()
	items = r.get('items', [])
	if not items:
		return {'ok': False, 'error': 'no channel'}
	it = items[0]
	ch = {'id': it['id'], 'title': it['snippet']['title'], 'subs': int(it['statistics'].get('subscriberCount', 0)), 'views_total': int(it['statistics'].get('viewCount', 0)), 'videos_total': int(it['statistics'].get('videoCount', 0))}
	uploads = it['contentDetails']['relatedPlaylists']['uploads']
	pl = yt.playlistItems().list(part='contentDetails', playlistId=uploads, maxResults=50).execute()
	vids = [x['contentDetails']['videoId'] for x in pl.get('items', [])]
	st = yt.videos().list(part='statistics,snippet,contentDetails', id=','.join(vids[:50])).execute()
	ranked = []
	for v in st.get('items', []):
		s = v.get('statistics', {})
		ranked.append({'id': v['id'], 'title': v['snippet']['title'][:100], 'published': v['snippet']['publishedAt'][:10], 'views': int(s.get('viewCount', 0)), 'likes': int(s.get('likeCount', 0)), 'comments': int(s.get('commentCount', 0))})
	ranked.sort(key=lambda x: x['views'], reverse=True)
	return {'ok': True, 'channel': ch, 'recent_count': len(vids), 'top': ranked[:15], 'recent_sum_views': sum(x['views'] for x in ranked), 'recent_sum_likes': sum(x['likes'] for x in ranked)}

def fetch_db_snapshot(limit=30):
	try:
		from pipeline import state
		c = state.connect()
		rows = c.execute('SELECT id, channel_id, youtube_id, title, view_count, like_count, published_at FROM publications ORDER BY published_at DESC LIMIT ?', (int(limit),)).fetchall()
		c.close()
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200], 'items': []}
	out = []
	for r in rows:
		try:
			out.append({'id': r['id'], 'ch': r['channel_id'], 'yt': r['youtube_id'], 'title': (r['title'] or '')[:100], 'views': int(r['view_count'] or 0), 'likes': int(r['like_count'] or 0), 'at': (r['published_at'] or '')[:10]})
		except Exception:
			pass
	return {'ok': True, 'items': out}

POS_WORDS = [
	'hay',
	'tuyet',
	'dep',
	'yeu',
	'thich',
	'dang yeu',
	'cute',
	'love',
	'great',
	'nice',
	'good',
	'amazing',
	'perfect',
	'khen',
	'cam on',
	'thanks',
	'wow',
	'hihi',
	'haha',
	':)',
	':D',
	'hay',
	'tuyệt',
	'đẹp',
	'yêu',
	'thích',
	'dễ thương',
	'đáng yêu',
	'cảm ơn',
	'khen',
	'xuất sắc',
	'tốt',
	'hay quá',
	'quá đỉnh',
	'đỉnh',
	'xinh',
	'ngầu',
	'chất',
	'vui',
]
NEG_WORDS = [
	'te',
	'xau',
	'chan',
	'do',
	'bad',
	'terrible',
	'boring',
	'hate',
	'ugly',
	'khong thich',
	'kho hieu',
	'nham',
	'sai',
	'tệ',
	'xấu',
	'chán',
	'dở',
	'không thích',
	'khó hiểu',
	'nhảm',
	'sai',
	'thất vọng',
	'dở tệ',
]

def _comments_block(cm):
	if not cm or not cm.get('ok'):
		return []
	tops = cm.get('top') or []
	if not tops:
		return []
	pos = 0
	neg = 0
	for c in tops:
		t = (c.get('text') or '').lower()
		if any(w in t for w in POS_WORDS):
			pos += 1
		elif any(w in t for w in NEG_WORDS):
			neg += 1
	out = ['== COMMENT TOP (theo like) ==']
	out.append('Tong ' + str(cm.get('count')) + ' cmt | Pos ' + str(pos) + ' / Neg ' + str(neg) + ' / Neutral ' + str(len(tops) - pos - neg))
	for c in tops[:12]:
		txt = (c.get('text') or '').replace(chr(10), ' ')[:120]
		out.append(str(c.get('likes')) + ' like: ' + txt)
	if pos > neg:
		out.append('TOM TAT: comment tich cuc, giu van phong hien tai')
	elif neg > pos:
		out.append('TOM TAT: co comment tieu cuc -> xem lai noi dung/hook')
	return out

def _analytics_block(an):
	if not an or not an.get('ok'):
		return []
	ch = an.get('channel') or {}
	out = []
	out.append('== ANALYTICS ' + str(an.get('window_days')) + ' NGAY (YouTube Analytics API) ==')
	if ch:
		v = ch.get('views')
		m = ch.get('estimatedMinutesWatched')
		pct = ch.get('averageViewPercentage')
		sg = ch.get('subscribersGained') or 0
		sl = ch.get('subscribersLost') or 0
		net = int(sg) - int(sl)
		out.append('Views: ' + str(v) + ' | Phut xem: ' + str(m) + ' | Avg retention: ' + str(pct) + '%')
		out.append('Subs: +' + str(sg) + ' / -' + str(sl) + ' -> NET ' + (('+') if net >= 0 else '') + str(net))
		if pct is not None:
			try:
				pf = float(pct)
				if pf >= 80:
					out.append('RETENTION: XUAT SAC (>=80%) - hook + noi dung giu chan tot')
				elif pf >= 60:
					out.append('RETENTION: TOT (60-80%) - con cho de tang')
				else:
					out.append('RETENTION: CAN CAI THIEN (<60%) - kiem tra hook 3s dau va do dai video')
			except Exception:
				pass
	tr = an.get('traffic') or []
	if tr:
		total = sum([int(x.get('views') or 0) for x in tr]) or 1
		parts = []
		for x in tr[:6]:
			try:
				pv = int(x.get('views') or 0)
				pct2 = round(100.0 * pv / total, 1)
				parts.append(str(x.get('source')) + '=' + str(pv) + '(' + str(pct2) + '%)')
			except Exception:
				parts.append(str(x.get('source')) + '=' + str(x.get('views')))
		out.append('Traffic (share): ' + ', '.join(parts))
		try:
			shorts_share = round(100.0 * sum([int(x.get('views') or 0) for x in tr if 'SHORTS' in str(x.get('source')).upper()]) / total, 1)
			if shorts_share >= 70:
				out.append('SHORTS chiem ' + str(shorts_share) + '% traffic -> tiep tuc dau tu format Shorts doc')
		except Exception:
			pass
	tv = an.get('top_by_watchtime') or []
	if tv:
		parts = []
		for x in tv[:5]:
			parts.append(str(x.get('video')) + '(' + str(x.get('minutes')) + 'm,' + str(x.get('avg_pct')) + '%)')
		out.append('Top watch-time (minutes retention): ' + ', '.join(parts))
		best_pct = [x for x in tv if x.get('avg_pct') and float(x.get('avg_pct')) >= 80]
		if best_pct:
			out.append('Video giu chan >=80%: ' + str(len(best_pct)) + ' -> pattern nay nen nhan rong')
	return out

def build_prompt(snap, db, kind=None):
	DQ = chr(34)
	ch = snap.get('channel', {})
	top = snap.get('top', [])[:10]
	lines = []
	lines.append('Ban la chuyen gia chien luoc YouTube Shorts. Phan tich kenh va de xuat noi dung TIENG VIET co dau.')
	lines.append('')
	lines.append('QUY TAC BAT BUOC:')
	lines.append('1. Doc ky TOP 10 video. Video top 1 gap 10x top 2 -> day la pattern chinh can nhan rong.')
	lines.append('2. Phan tich: video nao dang hieu qua? Chung co gi chung? (chu de, format, hook)')
	lines.append('3. Moi y tuong PHAI dua tren 1 video top cu the. VD neu top la meo -> de xuat cho/meo/thu cung.')
	lines.append('4. KHONG noi chung chung. KHONG khen subs/views. Tap trung vao CONTENT.')
	lines.append('5. KIND BAT BUOC = ' + str(kind) + '. Moi y tuong PHAI dung kind nay, KHONG doi the loai.')
	lines.append('')
	lines.append('== VI DU MAU (bat chuoc chat luong nay) ==')
	lines.append('Neu top1 la meo 12k views, top2 la AI 1k views:')
	lines.append(' summary: Top 1 (meo cam) gap 12x top 2, cho thay thu cung de thuong la content mạnh nhất. Các video con lai deu duoi 1.1k views, chua co pattern ro rang ngoai thu cung.')
	lines.append(' patterns: [thu cung de thuong (meo/cho) luon top, format 15-20s hook nhanh]')
	lines.append(' next_ideas: [{title: Meo cam gap gi khi thay dua leo, hook: Meo cam se phan ung the nao?, why: bam theo top1 meo cam}]')
	lines.append('')
	lines.append('== OUTPUT CUA BAN (JSON) ==')
	lines.append('')
	lines.append('== KENH ==')
	lines.append('Ten: ' + str(ch.get('title')))
	lines.append('Subs: ' + str(ch.get('subs')) + ' | Tong views: ' + str(ch.get('views_total')) + ' | Videos: ' + str(ch.get('videos_total')))
	lines.append('50 video gan nhat: ' + str(snap.get('recent_count')) + ' | Tong views: ' + str(snap.get('recent_sum_views')) + ' | Tong likes: ' + str(snap.get('recent_sum_likes')))
	lines.append('')
	lines.append('== TOP 10 VIDEO (theo views) ==')
	for i, v in enumerate(top, 1):
		lines.append(str(i) + '. [' + str(v['views']) + ' views, ' + str(v['likes']) + ' likes, ' + str(v['comments']) + ' cmt] ' + str(v['title']))
	lines.append('')
	an_lines = _analytics_block(snap.get('analytics'))
	cm_lines = _comments_block(snap.get('comments'))
	if cm_lines:
		lines.extend(cm_lines)
		lines.append('')
	if an_lines:
		lines.extend(an_lines)
		lines.append('')
	recent = (db.get('items') or [])[:5]
	if recent:
		lines.append('== 15 VIDEO DANG GAN NHAT (tu DB) ==')
		for i, v in enumerate(recent, 1):
			lines.append(str(i) + '. [' + str(v['views']) + 'v ' + str(v['likes']) + 'l] ' + str(v['title']))
		lines.append('')
	vref = snap.get('viral_ref') or []
	if vref:
		lines.append('')
		lines.append('== VIDEO VIRAL DANG HOT (tham khao pattern) ==')
		for v in vref[:6]:
			lines.append('- [' + str(v.get('views', 0)) + 'v] ' + str(v.get('title', ''))[:100])
		lines.append('Hay hoc pattern tu cac video tren (chu de, format, hook) nhung de xuat noi dung RIENG cho kenh nay.')
		if kind:
			lines.append('!!! UU TIEN: KIND = ' + str(kind) + '. De xuat PHAI thuoc the loai nay, dua tren TREND VIRAL o tren. BO QUA video top cua kenh neu khac the loai.')
			lines.append('Vi du: neu kind=anime thi de xuat ve anime/AMV/nhan vat anime, KHONG de xuat meo/cho.')
	lines.append('== YEU CAU ==')
	lines.append('Tra ve JSON 1 dong gom cac truong:')
	lines.append('{')
	lines.append(' ' + DQ + 'summary' + DQ + ': ' + DQ + '2-3 cau danh gia tong the hieu suat kenh' + DQ + ',')
	lines.append(' ' + DQ + 'strengths' + DQ + ': [' + DQ + 'diem manh 1' + DQ + ', ' + DQ + 'diem manh 2' + DQ + ', ' + DQ + 'diem manh 3' + DQ + '],')
	lines.append(' ' + DQ + 'weaknesses' + DQ + ': [' + DQ + 'diem yeu 1' + DQ + ', ' + DQ + 'diem yeu 2' + DQ + '],')
	lines.append(' ' + DQ + 'patterns' + DQ + ': [' + DQ + 'pattern hieu qua 1' + DQ + ', ' + DQ + 'pattern 2' + DQ + '],')
	lines.append(' ' + DQ + 'next_ideas' + DQ + ': [')
	lines.append(' {' + DQ + 'title' + DQ + ': ' + DQ + 'tieu de video <=80 ky tu' + DQ + ', ' + DQ + 'hook' + DQ + ': ' + DQ + 'cau hook 3 giay dau' + DQ + ', ' + DQ + 'why' + DQ + ': ' + DQ + 'ly do dua tren du lieu' + DQ + '},')
	lines.append(' {' + DQ + 'title' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'hook' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'why' + DQ + ': ' + DQ + '...' + DQ + '},')
	lines.append(' {' + DQ + 'title' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'hook' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'why' + DQ + ': ' + DQ + '...' + DQ + '},')
	lines.append(' {' + DQ + 'title' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'hook' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'why' + DQ + ': ' + DQ + '...' + DQ + '},')
	lines.append(' {' + DQ + 'title' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'hook' + DQ + ': ' + DQ + '...' + DQ + ', ' + DQ + 'why' + DQ + ': ' + DQ + '...' + DQ + '}')
	lines.append(' ],')
	lines.append(' ' + DQ + 'actions' + DQ + ': [' + DQ + 'hanh dong cu the 1' + DQ + ', ' + DQ + 'hanh dong cu the 2' + DQ + ', ' + DQ + 'hanh dong cu the 3' + DQ + ']')
	lines.append('}')
	lines.append('QUAN TRONG: tat ca text PHAI tieng Viet co dau. CHI tra ve JSON, khong giai thich.')
	return chr(10).join(lines)

def _parse_json(raw):
	import re
	if not raw:
		return None
	m = re.search(r'{.*}', raw, re.DOTALL)
	if not m:
		return None
	try:
		return json.loads(m.group(0))
	except Exception:
		return None

def analyze(channel_id=None, force=False, ttl=3600, ingest_kind=None, kind=None):
	if not force and os.path.exists(_cache_path(channel_id)):
		try:
			c = json.loads(open(_cache_path(channel_id), encoding='utf-8').read())
			if time.time() - float(c.get('ts', 0)) < ttl and c.get('advisor'):
				c['cached'] = True
				return c
		except Exception:
			pass
	snap = fetch_channel_snapshot(channel_id)
	db = fetch_db_snapshot()
	try:
		from ops import studio_analytics as sa
		snap['analytics'] = sa.fetch_analytics(channel_id=channel_id)
		try:
			snap['comments'] = sa.fetch_comments(channel_id=channel_id, limit=50)
		except Exception:
			snap['comments'] = {'ok': False}
	except Exception:
		snap['analytics'] = {'ok': False}
	if not snap.get('ok'):
		return {'ok': False, 'error': snap.get('error', 'yt fetch failed'), 'snapshot': snap}
	# Inject viral research trends vao snapshot
	try:
		from ops import viral_research as VR
		cached = VR.latest(1)
		if cached and cached[0].get('items'):
			vitems = cached[0]['items'][:8]
			snap['viral_ref'] = [{'title': str(x.get('title'))[:120], 'views': x.get('views')} for x in vitems]
	except Exception:
		pass
	prompt = build_prompt(snap, db, kind=kind)
	try:
		from ops import ai_content as ac
		raw = ac._call_ollama(prompt, temperature=0.5, max_tokens=900, timeout=300)
	except Exception as e:
		return {'ok': False, 'error': 'ollama: ' + str(e)[:200], 'snapshot': {'channel': snap.get('channel')}}
	parsed = _parse_json(raw)
	if not parsed:
		return {'ok': False, 'error': 'parse failed', 'raw': (raw or '')[:600]}
	payload = {'ok': True, 'ts': time.time(), 'cached': False, 'channel': snap.get('channel'), 'top5': snap.get('top', [])[:5], 'advisor': parsed, 'kind': kind}
	try:
		os.makedirs(os.path.dirname(CACHE), exist_ok=True)
		json.dump(payload, open(_cache_path(channel_id), 'w', encoding='utf-8'), ensure_ascii=False)
	except Exception:
		pass
	# luu lich su (chi khi force hoac chua co)
	try:
		import time as _t2
		hist_dir = os.path.join(ROOT, 'state', 'studio_history')
		os.makedirs(hist_dir, exist_ok=True)
		fn = _t2.strftime('%Y%m%d%H%M') + '.json'
		json.dump(payload, open(os.path.join(hist_dir, fn), 'w', encoding='utf-8'), ensure_ascii=False)
	except Exception:
		pass
	# Auto-post ideas vao topic_pool
	try:
		from ops import topic_pool as _tp
		kind = None
		if ingest_kind:
			kind = ingest_kind
		else:
			cht = (payload.get('channel') or {}).get('title', '')
			cl = cht.lower()
			kind = 'curiosity'
			if 'meo' in cl or 'pet' in cl:
				kind = 'cute_animals'
			elif 'food' in cl or 'am thuc' in cl:
				kind = 'food'
			elif 'dong vat' in cl or 'animal' in cl:
				kind = 'animals'
		k, added = _tp.ingest_advisor(payload, kind=kind)
		if added:
			payload['ingested'] = {'kind': k, 'added': added}
	except Exception:
		pass
	return payload

if __name__ == '__main__':
	r = analyze(force=True)
	print(json.dumps(r, ensure_ascii=False, default=str)[:2000].encode('ascii', 'replace').decode('ascii'))
