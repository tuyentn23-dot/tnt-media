# video_manager.py - quan ly video + SEO + analytics
import os, json, pickle
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM=os.path.join(ROOT,"memory")
PUB=os.path.join(MEM,"published.json")
TRACK=os.path.join(MEM,"video_tracking.json")
TOKEN=os.path.join(ROOT,"token.pickle")
def jload(p,d):
     try: return json.load(open(p,encoding="utf-8"))
     except Exception: return d
def svc():
     from google.auth.transport.requests import Request
     from googleapiclient.discovery import build
     d=pickle.load(open(TOKEN,"rb"))
     if d and d.expired and d.refresh_token: d.refresh(Request())
     return build("youtube","v3",credentials=d)
def sync():
     pubs=jload(PUB,[]).get("videos",[]) if isinstance(jload(PUB,[]),dict) else jload(PUB,[])
     ids=[v.get("youtube_id") for v in pubs if v.get("youtube_id")]
     if not ids: return []
     y=svc()
     r=y.videos().list(part="statistics,snippet,status",id=",".join(ids)).execute()
     out=[]
     for v in r.get("items",[]):
         out.append({"id":v["id"],"title":v["snippet"]["title"],"views":int(v.get("statistics",{}).get("viewCount",0)),"likes":int(v.get("statistics",{}).get("likeCount",0)),"comments":int(v.get("statistics",{}).get("commentCount",0)),"privacy":v["status"]["privacyStatus"],"published":v["snippet"]["publishedAt"][:10]})
     out.sort(key=lambda x:-x["views"])
     json.dump(out,open(TRACK,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
     return out
def pipeline():
 c=jload(os.path.join(ROOT,"memory","content_db.json"),dict())
 facts=c.get("facts",[])
 pv=jload(PUB,[])
 used=set(v.get("topic") for v in (pv.get("videos",[]) if isinstance(pv,dict) else []))
 un=[f for f in facts if f.get("topic") not in used]
 return {"total":len(facts),"unused":len(un)}

def summary():
    d=jload(TRACK,[])
    if not d: d=sync()
    import seo_analyzer as SA
    sa=SA.analyze()
    gs=jload(os.path.join(ROOT,"memory","growth_strategy.json"),dict())
    import glob as G
    tfs=sorted(G.glob(os.path.join(ROOT,"memory","trends","trend_*.json")))
    tr=jload(tfs[-1],dict()) if tfs else dict()
    return {"count":len(d),"total_views":sum(v["views"] for v in d),"total_likes":sum(v["likes"] for v in d),"avg_score":sa.get("avg_score",0),"need":sa.get("need",[]),"scored":sa.get("videos",[]),"growth":list(gs.get("phases",{}).keys()),"trend":tr.get("top_words",[])[:8],"pipeline":pipeline(),"videos":d}
if __name__=="__main__":
     import sys
     if "sync" in sys.argv: print(json.dumps(sync(),ensure_ascii=False,indent=1))
     else: print(json.dumps(summary(),ensure_ascii=False,indent=1))
