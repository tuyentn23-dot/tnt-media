# aimusic_short_pdca.py - render NEW shorts only, with lock + ledger
import os, sys, io, json, time, sqlite3
sys.path.insert(0, os.path.abspath("."))
os.environ["IMAGEIO_FFMPEG_EXE"]=os.path.abspath("tools/ffmpeg.exe")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from ops.content_video5 import load, build
from ops.content_freshness import signature, is_published, mark_published, published_count
from ops import os_publish
LOCK = "output/pdca.lock"
def _pid_alive(pid):
	import subprocess
	try:
		r = subprocess.run(["tasklist","/FI","PID eq "+str(pid),"/NH"],capture_output=True,text=True)
		return str(pid) in r.stdout
	except Exception:
		return False
def acquire_lock():
	if os.path.exists(LOCK):
		try:
			oldpid = int(open(LOCK).read().strip())
		except Exception:
			oldpid = 0
		if oldpid and _pid_alive(oldpid):
			print("LOCKED pid "+str(oldpid)+" running"); return False
		print("stale lock pid "+str(oldpid)+", removing")
		os.remove(LOCK)
	open(LOCK,"w").write(str(os.getpid()))
	return True
def release_lock():
	if os.path.exists(LOCK): os.remove(LOCK)
def publish_short(item, kind):
	out = os.path.abspath("output/short"+item["id"]+".mp4")
	build(item, out)
	title = (item["hook"] or "")[:90]
	desc = (item["body"]+" "+item.get("payoff",""))[:450]
	tags = [item["topic"], "shorts", "kham pha", "what if"]
	res = os_publish.publish(out, title, description=desc, tags=tags, privacy="public", topic="ashort_"+kind+"_"+item["id"], category_id="28", force=True)
	sig = signature(item, kind)
	mark_published(sig, {"youtube_id": res.get("youtube_id"), "topic": "ashort_"+kind+"_"+item["id"]})
	print("PUBLISHED", item["id"], res.get("youtube_id"))
	return res
def main():
	if not acquire_lock(): return
	try:
		kinds = ["whatif","facts"]
		limit = int(sys.argv[1]) if len(sys.argv)>1 else 3
		n = 0
		for kind in kinds:
			if n >= limit: break
			items = load(kind)
			for it in items:
				if n >= limit: break
				sig = signature(it, kind)
				if is_published(sig):
					print("SKIP", kind, it["id"]); continue
				try:
					publish_short(it, kind)
					n += 1
				except Exception as e:
					print("ERR", it["id"], str(e)[:150])
		print("DONE published", n, "ledger total", published_count())
	finally:
		release_lock()
if __name__ == "__main__":
	main()