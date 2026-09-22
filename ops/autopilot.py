# autopilot.py - tu dong chay PDCA theo lich, an toan, co log
import os, io, sys, json, time, subprocess, threading
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
CFG = os.path.join(ROOT,"memory","autopilot.json")
LOG = os.path.join(ROOT,"memory","autopilot_log.jsonl")
PY = sys.executable
LOCK = os.path.join(ROOT,"output","_pdca.lock")
try:
	from ops import evolve as _ev
except Exception:
	_ev = None

def _cfg():
	try:
		return json.load(io.open(CFG,encoding="utf-8"))
	except Exception:
		return {"enabled":False,"interval_min":180,"batch":3,"kinds":["whatif","facts"]}

def _save(c):
	io.open(CFG,"w",encoding="utf-8").write(json.dumps(c,ensure_ascii=False,indent=2))

def _log(ev):
	ev["ts"]=time.strftime("%Y-%m-%dT%H:%M:%S")
	io.open(LOG,"a",encoding="utf-8").write(json.dumps(ev,ensure_ascii=False)+chr(10))

def _pid_alive(pid):
	try:
		r=subprocess.run(["tasklist","/FI","PID eq "+str(pid),"/NH"],capture_output=True,text=True)
		return str(pid) in r.stdout
	except Exception:
		return False

def is_busy():
	if not os.path.exists(LOCK): return False
	try:
		pid=int(open(LOCK).read().strip())
	except Exception:
		return False
	return _pid_alive(pid)

def run_cycle():
	if is_busy():
		_log({"event":"skip_busy"}); return {"ok":False,"reason":"busy"}
	c=_cfg()
	batch=int(c.get("batch",3))
	r=subprocess.run([PY,"-X","utf8","ops/aimusic_short_pdca.py",str(batch)],cwd=ROOT,capture_output=True,text=True,timeout=3600)
	out=(r.stdout or "")[-2000:]
	_log({"event":"cycle_done","rc":r.returncode,"out":out})
	return {"ok":r.returncode==0,"out":out}

_stop=threading.Event()
_thread=None

def _loop():
	while not _stop.is_set():
		c=_cfg()
		if c.get("enabled"):
			try:
				if _ev: _ev.run_once()
				run_cycle()
			except Exception as e: _log({"event":"error","err":str(e)[:200]})
		iv=max(5,int(c.get("interval_min",180)))*60
		_stop.wait(iv)

def start():
	global _thread
	if _thread and _thread.is_alive(): return False
	_stop.clear()
	_thread=threading.Thread(target=_loop,daemon=True)
	_thread.start()
	_log({"event":"autopilot_started"})
	return True

def stop():
	_stop.set()
	_log({"event":"autopilot_stopped"})
	return True

def set_enabled(flag):
	c=_cfg(); c["enabled"]=bool(flag); _save(c)
	if flag: start()
	return c

def status():
	c=_cfg()
	return {"cfg":c,"busy":is_busy(),"thread_alive":bool(_thread and _thread.is_alive())}