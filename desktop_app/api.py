# -- coding: utf-8 --
# desktop_app/api.py - Client goi API server :7777
import json, urllib.request, urllib.error

BASE = 'http://127.0.0.1:7777'

def _req(method, path, body=None, timeout=3):
	url = BASE + path
	data = None
	if body is not None:
		data = json.dumps(body).encode('utf-8')
	req = urllib.request.Request(url, data=data, method=method)
	req.add_header('Content-Type', 'application/json')
	try:
		with urllib.request.urlopen(req, timeout=timeout) as r:
			raw = r.read().decode('utf-8')
			return json.loads(raw) if raw else {}
	except urllib.error.HTTPError as e:
		return {'ok': False, 'err': 'HTTP ' + str(e.code)}
	except Exception as e:
		return {'ok': False, 'err': str(e)}

def get(path, timeout=3):
	return _req('GET', path, None, timeout)

def post(path, body=None, timeout=15):
	return _req('POST', path, body, timeout)

def delete(path, timeout=3):
	return _req('DELETE', path, None, timeout)

_HEALTH_CACHE = {'t': 0, 'v': None}
def health():
	import time as _t
	now = _t.time()
	if _HEALTH_CACHE['v'] is not None and (now - _HEALTH_CACHE['t']) < 2.0:
		return _HEALTH_CACHE['v']
	r = get('/api/health', 2)
	if r and r.get('ok'):
		_HEALTH_CACHE['t'] = now
		_HEALTH_CACHE['v'] = r
	return r

def config():
	return get('/api/config')

def channels():
	return get('/api/channels')

def publications():
	return get('/api/publications')

def jobs():
	return get('/api/jobs')

def modules():
	return get('/api/modules')

def quota():
	return get('/api/quota')

def pending():
	return get('/api/pending')

def create_job(body):
	return post('/api/jobs', body)

def run_job(jid):
	return post('/api/jobs/' + str(jid) + '/run', timeout=900)

def delete_job(jid):
	return delete('/api/jobs/' + str(jid))

def approve(pid):
	return post('/api/publications/' + str(pid) + '/approve')

def reject(pid):
	return post('/api/publications/' + str(pid) + '/reject')

def selfcheck():
	return get('/api/diagnostics/selfcheck', 30)

def backup():
	return post('/api/backup', None, 60)

def voices():
	return get('/api/config/voices')

def presets():
	return get('/api/config/presets')

def kinds():
	return get('/api/config/kinds')

def job_detail(jid):
	return get('/api/jobs/' + str(jid))


def publications_queue(status=None, channel_id=None):
	qs = []
	if status:
		qs.append('status=' + str(status))
	if channel_id:
		qs.append('channel_id=' + str(channel_id))
	q = ('?' + '&'.join(qs)) if qs else ''
	return get('/api/publications/queue' + q)

def publish_pub(pid):
	return post('/api/publications/' + str(pid) + '/publish', timeout=600)

def schedule_pub(pid, at):
	return post('/api/publications/' + str(pid) + '/schedule', {'at': at})

def unschedule_pub(pid):
	return post('/api/publications/' + str(pid) + '/unschedule')


def bulk_publish(ids):
	return post('/api/publications/bulk_publish', {'ids': list(ids)}, timeout=1800)

def bulk_schedule(ids, at):
	return post('/api/publications/bulk_schedule', {'ids': list(ids), 'at': at})

def update_pub(pid, fields):
	return post('/api/publications/' + str(pid) + '/update', fields)


def ai_suggest(pid):
	return get('/api/ai/suggest/' + str(pid))

def ai_score(pid):
	return get('/api/ai/score/' + str(pid))

def ai_feedback(channel_id=None):
	q = ''
	if channel_id:
		q = '?channel_id=' + str(channel_id)
	return get('/api/ai/feedback' + q)
