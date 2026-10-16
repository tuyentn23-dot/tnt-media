# -- coding: utf-8 --
# ops/viral_research/social.py
# Lay metadata TikTok/Instagram/Facebook trending qua yt-dlp (khong tai video).
import json

PLATFORMS = ['tiktok', 'instagram', 'facebook']

PREFIX = {
	'tiktok': 'https://www.tiktok.com/tag/',
	'instagram': 'https://www.instagram.com/explore/tags/',
	'facebook': 'https://www.facebook.com/hashtag/',
}


def search_hashtag(platform, tag, max_results=20):
	import yt_dlp
	if platform not in PREFIX:
		return {'ok': False, 'error': 'platform not supported: ' + str(platform)}
	url = PREFIX[platform] + tag
	opts = {
		'quiet': True,
		'no_warnings': True,
		'skip_download': True,
		'extract_flat': True,
		'playlistend': max_results,
		'socket_timeout': 15,
	}
	items = []
	try:
		with yt_dlp.YoutubeDL(opts) as ydl:
			info = ydl.extract_info(url, download=False)
		for e in (info.get('entries') or [])[:max_results]:
			if not e:
				continue
			items.append({
				'id': e.get('id'),
				'title': e.get('title') or e.get('description', '')[:100],
				'channel': e.get('uploader') or e.get('channel'),
				'views': int(e.get('view_count') or 0),
				'likes': int(e.get('like_count') or 0),
				'duration_s': int(e.get('duration') or 0),
				'url': e.get('url') or e.get('webpage_url'),
				'platform': platform,
				'tag': tag,
			})
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200], 'items': items, 'platform': platform, 'tag': tag}
	return {'ok': True, 'items': items, 'platform': platform, 'tag': tag}


def discover_hashtags(platform, keywords, max_results=15):
	res = []
	for kw in keywords:
		tag = str(kw).strip().lower().replace(' ', '')
		if not tag:
			continue
		r = search_hashtag(platform, tag, max_results=max_results)
		res.append(r)
	return res
