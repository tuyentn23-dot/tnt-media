# seo_analyzer.py - cham diem SEO + de xuat
import os, json, pickle
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACK=os.path.join(ROOT,"memory","video_tracking.json")
def jload(p,d):
     try: return json.load(open(p,encoding="utf-8"))
     except Exception: return d
def score_video(v):
     score=0; issues=[]; tips=[]
     title=v.get("title","")
     views=v.get("views",0); likes=v.get("likes",0)
     if 30<=len(title)<=70: score+=25
     else: issues.append("Title 30-70 ky tu")
     if views>500: score+=25
     elif views>100: score+=15; tips.append("Chia se MXH tang view")
     else: tips.append("Can day view")
     er=(likes/views*100) if views else 0
     if er>3: score+=25
     elif er>1: score+=15
     else: tips.append("Them CTA like/comment")
     if v.get("privacy")=="public": score+=25
     return {"id":v.get("id"),"title":title,"score":score,"views":views,"er":round(er,1),"issues":issues,"tips":tips}
def analyze():
     vids=jload(TRACK,[])
     scored=[score_video(v) for v in vids]
     scored.sort(key=lambda x:-x["score"])
     avg=round(sum(s["score"] for s in scored)/len(scored)) if scored else 0
     acts=[]
     for s in scored:
         if s["score"]<75: acts.append(s)
     return {"avg_score":avg,"videos":scored,"need":acts[:3]}
if __name__=="__main__":
     import json
     print(json.dumps(analyze(),ensure_ascii=False,indent=1))
