import subprocess, sys, time, urllib.request, os
proc = subprocess.Popen([sys.executable, 'ops/state_api.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)
try:
 r = urllib.request.urlopen('http://127.0.0.1:8765/state/latest', timeout=5)
 print('STATUS', r.status)
 print(r.read().decode('utf-8')[:800])
except Exception as e:
 print('ERR', type(e).name, e)
 out, err = proc.communicate(timeout=2) if proc.poll() is not None else (b'', b'')
 print('STDOUT', out.decode('utf-8', 'ignore')[:500])
 print('STDERR', err.decode('utf-8', 'ignore')[:500])
finally:
 proc.terminate()
