import subprocess, sys, time, urllib.request
proc = subprocess.Popen([sys.executable, 'ops/state_api.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
time.sleep(3)
lines = []
try:
 r = urllib.request.urlopen('http://127.0.0.1:8765/state/latest', timeout=5)
 print('HTTP', r.status)
 print(r.read().decode('utf-8')[:1200])
except Exception as e:
 print('REQ-ERR', type(e).name, str(e)[:200])
finally:
 proc.terminate()
 try:
 o, x = proc.communicate(timeout=2)
 print('PROC-OUT:')
 print((o or '')[:1500])
 except Exception:
 proc.kill()
