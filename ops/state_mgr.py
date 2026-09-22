# ops/state_mgr.py - quan ly STATE.md (doc/ghi/append video)
import os, sys, re, time
sys.path.insert(0, os.getcwd())
STATE_FILE = "STATE.md"

def read():
	if not os.path.exists(STATE_FILE):
		return ""
	return open(STATE_FILE, encoding="utf-8").read()

def write(content):
	open(STATE_FILE, "w", encoding="utf-8").write(content)

def check():
	# Kiem tra STATE.md co du section chinh khong
	src = read()
	required = ["## KENH", "## TOOLS CHINH", "## TODO", "## CANH BAO"]
	missing = [s for s in required if s not in src]
	ok = len(missing) == 0
	return {"ok": ok, "missing": missing, "size": len(src), "lines": src.count(chr(10))}

def append_publish(channel, vid_id, title, ts=None):
	ts = ts or time.strftime("%Y-%m-%d %H:%M")
	line = chr(45) + " [" + channel + "] " + vid_id + " - " + title
	logfile = "output/publish_log.md"
	os.makedirs("output", exist_ok=True)
	with open(logfile, "a", encoding="utf-8") as f:
		f.write(ts + " | " + line + chr(10))
	return logfile

if __name__ == "__main__":
	import sys as _s
	cmd = _s.argv[1] if len(_s.argv) > 1 else "check"
	if cmd == "check":
		r = check()
		print("OK" if r["ok"] else "FAIL", r)
	elif cmd == "show":
		print(read()[:500])