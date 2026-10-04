# -- coding: utf-8 --
# Daily scheduler - tu dong san xuat + dang 4 video/ngay/kenh
import os, sys, json, time, sqlite3, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ops import produce as pd
from ops import upload_short as us

# Map topic -> library folder
def topic_to_folder(topic):
	m = {
		'anime': 'anime',
		'roblox': 'roblox',
		'cute_animals': 'cute_animals',
		'gacha': 'gacha',
		'lifestyle': 'lifestyle',
		'food': 'food',
		'nostalgia': 'nostalgia',
		'facts': 'facts',
		'curiosity': 'curiosity',
		'psychology': 'psychology',
		'whatif': 'whatif',
		'science': 'science',
		'nature': 'nature',
	}
	return m.get(topic, topic)

# Channel configs
CHANNELS = {
	'Mialinhcute': {
		'themes': ['pink', 'purple', 'gold', 'blue'],
		'topics': ['anime', 'roblox', 'cute_animals', 'gacha'],
		'hashtags': ['#Shorts', '#MiaLinhCute', '#animation'],
	},
	'vilevi5676': {
		'themes': ['blue', 'orange', 'gold', 'purple'],
		'topics': ['lifestyle', 'food', 'nostalgia', 'facts', 'curiosity', 'psychology', 'whatif', 'science', 'nature'],
		'hashtags': ['#Shorts', '#ViLeVi', '#vlog'],
	},
}

def produce_batch(channel, batch_size=4, privacy='unlisted'):
	"""San xuat batch_size video cho channel, return list paths + metadata."""
	cfg = CHANNELS.get(channel)
	if not cfg:
		return []
	
	used = us._used_topics(channel, 30)
	available = [t for t in cfg['topics'] if t not in used]
	if len(available) < batch_size:
		# reset neu het topic
		available = list(cfg['topics'])
	random.shuffle(available)
	picked = available[:batch_size]
	
	out_dir = 'media/' + channel
	os.makedirs(out_dir, exist_ok=True)
	ts = int(time.time())
	
	results = []
	for i, topic in enumerate(picked):
		folder = topic_to_folder(topic)
		theme = cfg['themes'][i % len(cfg['themes'])]
		out_path = os.path.join(out_dir, topic + '' + str(ts) + '.mp4')
		
		try:
			r = pd.make(folder, topic, out_path, theme=theme, aspect='9:16', n=6, seg=2.0)
			if r.get('ok'):
				title = r['hook'][:60]
				tags = [channel.lower(), topic] + [h.lstrip('#') for h in cfg['hashtags']]
				desc = title + chr(10) + chr(10) + ' '.join(cfg['hashtags'])
				results.append({
					'topic': topic,
					'path': out_path,
					'title': title,
					'tags': tags,
					'description': desc,
					'dur': r['dur'],
					'qc': r['qc'],
				})
				print('[batch] OK ' + channel + ' ' + topic + ' -> ' + out_path, flush=True)
			else:
				print('[batch] FAIL ' + topic + ': ' + str(r), flush=True)
		except Exception as e:
			print('[batch] ERROR ' + topic + ': ' + str(e)[:200], flush=True)
	
	return results

def publish_batch(channel, items, privacy='public'):
	"""Dang batch video len YouTube."""
	results = []
	for it in items:
		try:
			r = us.publish(
				video_path=it['path'],
				title=it['title'],
				description=it['description'],
				tags=it['tags'],
				channel=channel,
				topic=it['topic'],
				privacy=privacy,
			)
			r['topic'] = it['topic']
			r['file'] = it['path']
			results.append(r)
			print('[publish] ' + it['topic'] + ': ' + str(r.get('ok')), flush=True)
		except Exception as e:
			print('[publish] ERROR ' + it['topic'] + ': ' + str(e)[:200], flush=True)
			results.append({'ok': False, 'topic': it['topic'], 'err': str(e)[:200]})
	return results
