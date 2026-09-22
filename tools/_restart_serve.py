import subprocess, re, time, os, signal
try:
    out = subprocess.run(['netstat','-ano'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
    pids = set()
    for line in out.splitlines():
        if ':8787' in line and 'LISTENING' in line:
            parts = line.split()
            pids.add(parts[-1])
    for pid in pids:
        try:
            subprocess.run(['taskkill','/F','/PID', pid], capture_output=True)
            print('killed', pid)
        except Exception as e:
            print('kill err', pid, e)
except Exception as e:
    print('scan err', e)
time.sleep(3)
subprocess.Popen(['python','_serve.py'], cwd=os.getcwd(), creationflags=0x00000008)
print('restarted')
