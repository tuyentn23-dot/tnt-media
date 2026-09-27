# -- coding: utf-8 --
# Mass publish: 4 video moi kenh, dung style tung kenh
import os, sys, time, json, urllib.request
sys.path.insert(0, os.getcwd())
BASE = 'http://127.0.0.1:7777'
CHANNELS = [
	'Mialinhcute',
	'vilevi5676',
]
PER = 4

def api(path, method='GET', body=None):
	url = BASE + path
	data = json.dumps(body).encode() if body else None
	req = urllib.request.Request(url, data=data, method=method)
	if body:
		req.add_header('Content-Type', 'application/json')
	return json.loads(urllib.request.urlopen(req, timeout=30).read())

def wait_job(jid, max_sec=600):
	t0 = time.time()
	while time.time() - t0 < max_sec:
		time.sleep(10)
		r = api('/api/jobs?limit=30')
		for it in r.get('items', []):
			if it.get('id') == jid:
				st = it.get('status')
				if st in ('pending_approval', 'done', 'failed'):
					return st
	return 'timeout'

def publish_pending(channel):
	r = api('/api/publications?limit=100')
	published = []
	for it in r.get('items', []):
		if it.get('channel_id') != channel:
			continue
		if it.get('status') == 'published':
			continue
		pid = it.get('id')
		st = it.get('status')
		if st in ('rendered', 'pending'):
			try:
				api('/api/publications/' + str(pid) + '/approve', method='POST')
			except Exception as e:
				print(' approve fail:', str(e)[:80])
		try:
			res = api('/api/publications/' + str(pid) + '/publish', method='POST')
			print(' pub', pid, '->', res)
			published.append(pid)
		except Exception as e:
			print(' pub fail:', pid, str(e)[:120])
	return published

def main():
	for channel in CHANNELS:
		print()
		print('==== ' + channel + ' ====')
		for i in range(PER):
			body = {'channel_id': channel, 'count': 1}
			try:
				r = api('/api/jobs', method='POST', body=body)
				jid = r.get('job_id')
				print('[' + channel + '] job ', i+1, '/', PER, ': ', jid)
				api('/api/jobs/' + jid + '/run', method='POST')
				st = wait_job(jid, max_sec=600)
				print(' -> ', st)
			except Exception as e:
				print('ERR ', i, str(e)[:120])
		print('Publishing pending for ', channel)
		pubs = publish_pending(channel)
		print('Published ', len(pubs), ' pubs: ', pubs)

if __name__ == '__main__':
	main()
