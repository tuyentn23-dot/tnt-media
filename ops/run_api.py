import subprocess, sys, os
log = open('api.log', 'w', encoding='utf-8')
p = subprocess.Popen([sys.executable, 'ops/state_api.py'], stdout=log, stderr=subprocess.STDOUT, creationflags=0x00000008 | 0x00000200)
print('PID', p.pid)
