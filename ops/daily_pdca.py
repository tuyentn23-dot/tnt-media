# daily_pdca.py - run one full cycle: render new content -> publish -> measure
# Schedule this 2-3x/day via Windows Task Scheduler for full autopilot
import os,sys,json,glob,subprocess
ROOT=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,ROOT)
PY=sys.executable
def sh(script,args=None,timeout=3600):
    env=dict(os.environ); env["PYTHONPATH"]=ROOT
    try:
        r=subprocess.run([PY,script]+(args or []),cwd=ROOT,env=env,capture_output=True,text=True,timeout=timeout)
        return r.returncode
    except Exception as e:
        print("ERR",e); return 1
def main():
    print("DAILY PDCA")
    # DO: render all content to daily_ prefix
    from ops.content_video5 import load, build
    def rend(kind):
        return [build(it, ROOT+"/output/daily_"+it["id"]+".mp4") for it in load(kind)]
    rend("whatif"); rend("facts")
    print("rendered")
    # CHECK
    sh("ops/perf_tracker.py")
    print("done")
if __name__ == "__main__":
    main()
