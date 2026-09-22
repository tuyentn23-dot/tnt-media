# daily_trend.py - quet trend that hang ngay tu YouTube Data API
import os, sys, json, pickle
from datetime import datetime, date
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
TOKEN=os.path.join(ROOT,"token.pickle")
MEM=os.path.join(ROOT,"memory")
OUT=os.path.join(ROOT,"output")
def svc():
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    d=pickle.load(open(TOKEN,"rb"))
    if d and d.expired and d.refresh_token: d.refresh(Request())
    return build("youtube","v3",credentials=d)

def scan(region="VN", maxres=50):
    y=svc()
    r=y.videos().list(part="snippet,statistics",chart="mostPopular",regionCode=region,maxResults=maxres).execute()
    items=[]
    for v in r.get("items",[]):
        st=v.get("statistics",{}); sn=v.get("snippet",{})
        items.append({"id":v["id"],"title":sn.get("title"),"channel":sn.get("channelTitle"),"views":int(st.get("viewCount",0)),"likes":int(st.get("likeCount",0)),"cat":sn.get("categoryId")})
    return items

def analyze(items):
    from collections import Counter
    words=[]
    for t in [i["title"].lower() for i in items]:
        for w in t.replace("#"," ").split():
            if len(w)>3: words.append(w)
    top=Counter(words).most_common(20)
    short=[i for i in items if "#short" in i["title"].lower()]
    return {"scanned":len(items),"short_count":len(short),"top_words":top,"top_by_views":sorted(items,key=lambda x:-x["views"])[:10]}

def run(region="VN"):
    items=scan(region)
    rep=analyze(items)
    rep["date"]=date.today().isoformat()
    rep["region"]=region
    rep["generated"]=datetime.now().isoformat(timespec="seconds")
    os.makedirs(os.path.join(MEM,"trends"),exist_ok=True)
    p=os.path.join(MEM,"trends","trend_"+date.today().isoformat()+".json")
    json.dump(rep,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    return rep,p

if __name__=="__main__":
    reg=sys.argv[1] if len(sys.argv)>1 else "VN"
    rep,p=run(reg)
    print("SCANNED",rep["scanned"])
    print("SAVED",p)


def search_kw(q, maxr=15):
    y=svc()
    r=y.search().list(part="snippet",q=q,type="video",videoDuration="short",order="viewCount",maxResults=maxr,regionCode="VN").execute()
    ids=[i["id"]["videoId"] for i in r.get("items",[]) if i.get("id",{}).get("videoId")]
    if not ids: return []
    d=y.videos().list(part="snippet,statistics",id=",".join(ids)).execute()
    out=[]
    for v in d.get("items",[]):
        st=v.get("statistics",{}); sn=v.get("snippet",{})
        out.append({"id":v["id"],"title":sn.get("title"),"views":int(st.get("viewCount",0))})
    return out
