import os, sys, subprocess, time, json, urllib.request
U = chr(95)
DDU = U + U
ROOT = 'D:/TNT_AI/venture_foundry/media'
PROFILE = os.path.join(ROOT, 'flow_chrome_clean')
CHROME_CANDIDATES = [
	'C:/Program Files/Google/Chrome/Application/chrome.exe',
	'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
	os.path.expanduser('~/AppData/Local/Google/Chrome/Application/chrome.exe'),
]
CHROME = None
for c in CHROME_CANDIDATES:
	if os.path.exists(c):
		CHROME = c
		break
if not CHROME:
	print('CHROME NOT FOUND')
	sys.exit(1)
print('CHROME:', CHROME)
PORT = '9222'
URL = 'https://flow.google.com/'
os.makedirs(PROFILE, exist_ok=True)
# Kiem tra CDP da chay chua
def cdp_alive():
	try:
		urllib.request.urlopen('http://127.0.0.1:' + PORT + '/json/version', timeout=2)
		return True
	except Exception:
		return False

if cdp_alive():
	print('CDP already alive')
else:
	args = [CHROME, '--remote-debugging-port=' + PORT, '--user-data-dir=' + PROFILE, '--no-first-run', '--no-default-browser-check', URL]
	CREATE_NEW_GROUP = 0x00000200
	CREATE_NO_WINDOW = 0x08000000
	p = subprocess.Popen(args, creationflags=CREATE_NEW_GROUP | CREATE_NO_WINDOW)
	print('launched chrome pid', p.pid)
	time.sleep(8)

if cdp_alive():
	d = json.loads(urllib.request.urlopen('http://127.0.0.1:' + PORT + '/json/version', timeout=5).read())
	print('CDP OK:', d.get('Browser'))
	tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:' + PORT + '/json/list', timeout=5).read())
	for t in tabs:
		u = t.get('url', '')
		if 'flow.google.com' in u or 'google.com' in u:
			print('tab:', u[:120])
else:
	print('CDP FAILED to start')
