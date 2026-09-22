# media_cleaner.py - auto-cleanup media to prevent disk bloat
# Rules: delete used outputs, keep only best clips/topic, remove temp
import os,sys,json,glob,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)

def rm(p):
    try: os.remove(p); return True
    except: return False

def clean_output(keep="published"):
    # delete output videos already published (they live on YouTube)
    pub=json.load(open(os.path.join(ROOT,"memory","published.json"),encoding="utf-8"))
    used={os.path.basename(v.get("file","")) for v in pub["videos"] if v.get("file")}
    deleted=[]
    for f in glob.glob(os.path.join(ROOT,"output",".mp4")):
        if os.path.basename(f) in used and rm(f): deleted.append(os.path.basename(f))
    return deleted

def clean_trash():
    t=os.path.join(ROOT,"_trash")
    if not os.path.isdir(t): return 0
    return sum(1 for f in os.listdir(t) if rm(os.path.join(t,f)))

def clean_temp():
    n=0
    for pat in ["_.py","*.log",".json","_.txt","TEMP"]:
        for f in glob.glob(os.path.join(ROOT,pat)): n+=rm(f)
    return n

def clean_library(max_per_topic=2):
    lib=os.path.join(ROOT,"library")
    if not os.path.isdir(lib): return 0
    import json as j
    tops=[t for t in os.listdir(lib) if os.path.isdir(os.path.join(lib,t))]
    def keep(t):
        d=os.path.join(lib,t); mp=os.path.join(d,"_manifest.json")
        m=j.load(open(mp,encoding="utf-8")) if os.path.exists(mp) else []
        m=sorted(m,key=lambda e:e.get("score",0),reverse=True)
        k={e["file"] for e in m[:max_per_topic]}
        mp4s=sorted([f for f in os.listdir(d) if f.endswith(".mp4")],key=lambda f:os.path.getsize(os.path.join(d,f)))
        return k if k else set(mp4s[:max_per_topic])
    def dt(t):
        d=os.path.join(lib,t); k=keep(t)
        return sum(1 for f in os.listdir(d) if f.endswith(".mp4") and f not in k and rm(os.path.join(d,f)))
    return sum(dt(t) for t in tops)
def report():
    allf=[os.path.join(r,f) for r,d,fs in os.walk(ROOT) if ".git" not in r and "pycache" not in r for f in fs]
    sz=sum(os.path.getsize(p) for p in allf if os.path.isfile(p))
    return round(sz/1024/1024,1)

if __name__ == "__main__":
    print("before:",report(),"MB")
    print("output cleaned:",len(clean_output()))
    print("trash cleaned:",clean_trash())
    print("temp cleaned:",clean_temp())
    print("library trimmed:",clean_library())
    print("after:",report(),"MB")
