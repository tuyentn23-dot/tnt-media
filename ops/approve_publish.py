# -- coding: utf-8 --
# Approve va publish 8 video moi voi privacy=public
import sys, os, json, urllib.request, urllib.error
sys.path.insert(0, '.')
from pipeline import state

API = 'http://127.0.0.1:7777'

c = state.connect()
rows = c.execute("SELECT id, channel_id, file_path, title FROM publications WHERE signature LIKE 'pub_%' AND status='rendered' ORDER BY id").fetchall()
print('pending:', len(rows))

for r in rows:
	pid = r['id']
	print('---', pid, r['channel_id'], os.path.basename(r['file_path']))
	# approve
	try:
		req = urllib.request.Request(API + '/api/publications/' + str(pid) + '/approve', data=b'', method='POST')
		r2 = urllib.request.urlopen(req, timeout=10)
		print(' approve:', r2.read().decode())
	except urllib.error.HTTPError as e:
		print(' approve FAIL:', e.code, e.read()[:100])
		continue
	# publish public
	try:
		req = urllib.request.Request(API + '/api/publications/' + str(pid) + '/publish?privacy=public', data=b'', method='POST')
		r3 = urllib.request.urlopen(req, timeout=180)
		print(' publish:', r3.read().decode())
	except urllib.error.HTTPError as e:
		print(' publish FAIL:', e.code, e.read()[:300])
	except Exception as e:
		print(' publish EXC:', str(e)[:200])

print('DONE')
