# -- coding: utf-8 --
# ops/viral_research/youtube.py
# Lay metadata video viral YouTube (khong tai video) qua yt-dlp hoac API key.
import os, json, time, urllib.request
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'


def _api_key():
	for line in open('.env', encoding='utf-8'):
		line = line.strip()
		if line.startswith('YOUTUBE_API_KEY='):
			return line.split('=', 1)[1].strip()
	return os.environ.get('YOUTUBE_API_KEY', '').strip()


def via_api(region='VN', max_results=30, category=None):
	key = _api_key()
	if not key:
		return {'ok': False, 'error': 'YOUTUBE_API_KEY not set'}
	url = ('https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails'
		+ '&chart=mostPopular&regionCode=' + region
		+ '&maxResults=' + str(min(50, max_results))
		+ (('&videoCategoryId=' + str(category)) if category else '')
		+ '&key=' + key)
	try:
		req = urllib.request.Request(url, headers={'User-Agent': UA})
		r = urllib.request.urlopen(req, timeout=20)
		d = json.loads(r.read().decode('utf-8'))
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}
	items = []
	for it in d.get('items', []):
		sn = it.get('snippet', {})
		st = it.get('statistics', {})
		cd = it.get('contentDetails', {})
		items.append({
			'id': it.get('id'),
			'title': sn.get('title'),
			'channel': sn.get('channelTitle'),
			'published': sn.get('publishedAt'),
			'category_id': sn.get('categoryId'),
			'tags': sn.get('tags', [])[:8],
			'thumb': (sn.get('thumbnails', {}).get('high') or {}).get('url'),
			'views': int(st.get('viewCount', 0)),
			'likes': int(st.get('likeCount', 0)),
			'comments': int(st.get('commentCount', 0)),
			'duration': cd.get('duration'),
			'platform': 'youtube',
		})
	return {'ok': True, 'items': items, 'source': 'api'}


def search(query, max_results=20, platform='youtube'):
	import yt_dlp
	opts = {
		'quiet': True,
		'no_warnings': True,
		'skip_download': True,
		'extract_flat': True,
		'playlistend': max_results,
		'socket_timeout': 15,
	}
	if platform == 'youtube':
		url = 'ytsearch' + str(max_results) + ':' + query + ' shorts'
	else:
		url = 'ytsearch' + str(max_results) + ':' + query
	items = []
	try:
		with yt_dlp.YoutubeDL(opts) as ydl:
			info = ydl.extract_info(url, download=False)
		for e in (info.get('entries') or []):
			if not e:
				continue
			items.append({
				'id': e.get('id'),
				'title': e.get('title'),
				'channel': e.get('uploader') or e.get('channel'),
				'views': int(e.get('view_count') or 0),
				'duration_s': int(e.get('duration') or 0),
				'url': e.get('url') or ('https://youtube.com/watch?v=' + str(e.get('id'))),
				'platform': platform,
			})
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200], 'items': items}
	return {'ok': True, 'items': items, 'query': query, 'source': 'yt-dlp'}


def only_shorts(items):
	# Shorts = duration <= 60s (hoac 180s theo chuan moi)
	out = []
	for it in items or []:
		d = int(it.get('duration_s') or 0)
		if d and d <= 180:
			out.append(it)
	return out


def shorts_search(query, max_results=20):
	r = search(query + ' shorts', max_results=max_results)
	if r.get('ok'):
		r['items'] = only_shorts(r.get('items', []))
		r['shorts_filtered'] = True
	return r
