# -- coding: utf-8 --
# Mo Chrome that voi remote-debugging de dung cho vids_agent / automation.
# Sau khi chay: dang nhap Google trong cua so Chrome, roi chay vids_agent.generate().
import os, subprocess, time, json, urllib.request
PROFILE = os.path.join(os.path.dirname(os.path.abspath(file)), '_vids_chrome')
CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
PORT = '9222'

def launch(url='https://vids.new'):
    os.makedirs(PROFILE, exist_ok=True)
    args = [CHROME, '--remote-debugging-port=' + PORT, '--user-data-dir=' + PROFILE, '--no-first-run', '--no-default-browser-check', url]
    subprocess.Popen(args)
    time.sleep(7)
    try:
     d = json.load(urllib.request.urlopen('http://127.0.0.1:' + PORT + '/json/version'))
     return {'ok': True, 'browser': d.get('Browser')}
    except Exception as e:
     return {'ok': False, 'error': str(e)}

if name == 'main':
    print(launch())
