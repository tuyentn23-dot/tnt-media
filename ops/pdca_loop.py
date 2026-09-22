# pdca_loop.py - continuous Plan-Do-Check-Act cycle
import os, sys, json, time, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
LOG = os.path.join(ROOT, "memory", "pdca_log.json")
def log(msg):
    d = json.load(open(LOG,encoding="utf-8")) if os.path.exists(LOG) else {"events":[]}
    d["events"].append({"t":time.strftime("%Y-%m-%d %H:%M"),"msg":msg})
    json.dump(d,open(LOG,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    print(msg)
def run(script,args=None):
    env=dict(os.environ); env["PYTHONPATH"]=ROOT
    try:
        r=subprocess.run([sys.executable,script]+(args or []),cwd=ROOT,capture_output=True,text=True,timeout=1800,env=env)
        return r.returncode==0, r.stdout[-500:]
    except Exception as e:
        return False, str(e)
if __name__ == "__main__":
    log("PDCA start")
    o1,r1=run("ops/scheduler.py"); log("DO scheduler "+str(o1))
    o2,r2=run("ops/perf_tracker.py"); log("CHECK perf "+str(o2))
    log("ACT review winners")
    log("PDCA done")
