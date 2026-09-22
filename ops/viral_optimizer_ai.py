# viral_optimizer_ai.py - self-learning performance optimizer
import os,sys,json,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
PERF=os.path.join(ROOT,"memory","performance.json")
BRAIN=os.path.join(ROOT,"memory","viral_brain.json")
def load(p,d=None):
    try: return json.load(open(p,encoding="utf-8"))
    except: return d if d is not None else {}
def score_video(v):
    views=v.get("views",0); likes=v.get("likes",0); comments=v.get("comments",0)
    if views==0: return 0.0
    return round(views*0.5 + likes*10 + comments*50, 1)
def analyze():
    perf=load(PERF,[])
    seen={}
    for v in perf:
        i=v.get("id")
        if i and (i not in seen or v.get("views",0)>seen[i].get("views",0)): seen[i]=v
    vids=list(seen.values())
    for v in vids: v["score"]=score_video(v)
    vids.sort(key=lambda x:-x["score"])
    return vids
def learn():
    vids=analyze()
    winners=[v for v in vids if v.get("score",0)>500][:10]
    losers=[v for v in vids if 0<v.get("score",0)<50]
    brain={"updated":time.strftime("%Y-%m-%d %H:%M"),"winners":winners,"losers":len(losers),"total":len(vids)}
    json.dump(brain,open(BRAIN,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    return brain
if __name__ == "__main__":
    b=learn()
    print("done", len(b["winners"]))
