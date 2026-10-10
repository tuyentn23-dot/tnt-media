# -- coding: utf-8 --
# desktop_app/api.py - Client goi API server :7777
import json, urllib.request, urllib.error

BASE = 'http://127.0.0.1:7777'

def _req(method, path, body=None, timeout=8):
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

def get(path, timeout=8):
	return _req('GET', path, None, timeout)

def post(path, body=None, timeout=20):
	return _req('POST', path, body, timeout)

def delete(path, timeout=8):
	return _req('DELETE', path, None, timeout)

def health():
	return get('/api/health', 3)

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
	return post('/api/jobs/' + str(jid) + '/run')

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
	return post('/api/publications/' + str(pid) + '/publish')

def schedule_pub(pid, at):
	return post('/api/publications/' + str(pid) + '/schedule', {'at': at})

def unschedule_pub(pid):
	return post('/api/publications/' + str(pid) + '/unschedule')
