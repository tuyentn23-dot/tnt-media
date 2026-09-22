# master_viral.py - full autonomous pipeline
# generate -> render -> SEO -> publish -> measure -> adapt (loop)
import os,sys,json,time,subprocess,glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
PY=sys.executable
def sh(s,args=None,t=3600):
    env=dict(os.environ); env["PYTHONPATH"]=ROOT
    try:
        r=subprocess.run([PY,s]+(args or []),cwd=ROOT,env=env,timeout=t,capture_output=True,text=True)
        return r.returncode
    except Exception as e: print("ERR",s,str(e)[:80]); return 1
def main():
    print("MASTER VIRAL PIPELINE")
    # CHECK (measure)
    sh("ops/perf_tracker.py")
    sh("ops/viral_engine_auto.py")
    # show brain
    try:
        b=json.load(open(ROOT+"/memory/viral_brain.json"))
        print("winners:",len(b.get("winners",[])))
    except: pass
    print("pipeline done")
if __name__ == "__main__":
    main()
