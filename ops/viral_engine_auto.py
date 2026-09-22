# viral_engine_auto.py - THE AUTONOMOUS VIRAL ALGORITHM
# cycle: measure -> learn winners -> generate new -> publish -> repeat
import os,sys,json,time,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
PY=sys.executable
def sh(script,args=None,t=1800):
    env=dict(os.environ); env["PYTHONPATH"]=ROOT
    try: subprocess.run([PY,script]+(args or []),cwd=ROOT,env=env,timeout=t,capture_output=True)
    except Exception as e: print("ERR",script,e)
def cycle():
    print("=== VIRAL CYCLE "+time.strftime("%H:%M")+" ===")
    # 1 MEASURE
    sh("ops/perf_tracker.py")
    # 2 LEARN
    sh("ops/viral_optimizer_ai.py")
    # 3 read brain
    try:
        b=json.load(open(ROOT+"/memory/viral_brain.json"))
        print("winners:",len(b.get("winners",[])),"total:",b.get("total"))
    except: pass
    print("cycle done")
if __name__ == "__main__":
    cycle()
