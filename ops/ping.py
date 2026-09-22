import urllib.request, traceback
try:
 r = urllib.request.urlopen('http://127.0.0.1:8765/state/latest', timeout=5)
 print('STATUS', r.status)
 print(r.read().decode('utf-8')[:1500])
except Exception as e:
 print('ERR', type(e).name)
 traceback.print_exc()
