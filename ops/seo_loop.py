# seo_loop.py - continuous SEO optimizer for all videos
import os,sys,json,time,pickle
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
def yt():
    d=pickle.load(open(os.path.join(ROOT,"token.pickle"),"rb"))
    if d and d.expired and d.refresh_token: d.refresh(Request())
    return build("youtube","v3",credentials=d)
def has_seo(sn):
    ok = bool(sn.get("tags")) and len(sn.get("description",""))>80 and "#shorts" in sn.get("title","")
    return ok
def audit():
    y=yt()
    pub=json.load(open(os.path.join(ROOT,"memory","published.json"),encoding="utf-8"))
    ids=[v["youtube_id"] for v in pub["videos"] if v.get("youtube_id")][-50:]
    r=y.videos().list(part="snippet",id=",".join(ids)).execute()
    bad=[]
    for v in r.get("items",[]):
        if not has_seo(v["snippet"]): bad.append(v["id"])
    return bad
if __name__ == "__main__":
    bad=audit()
    print("videos needing SEO:",len(bad))