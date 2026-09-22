# channel_stats.py - fetch REAL stats from YouTube for active channel
import os,sys,json,pickle
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
def yt():
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    d=pickle.load(open(os.path.join(ROOT,"token.pickle"),"rb"))
    if d and d.expired and d.refresh_token: d.refresh(Request())
    return build("youtube","v3",credentials=d)
def stats():
    y=yt()
    ch=y.channels().list(part="snippet,statistics",mine=True).execute()
    c=ch["items"][0]
    return {"id":c["id"],"title":c["snippet"]["title"],"subs":int(c["statistics"].get("subscriberCount",0)),"views":int(c["statistics"].get("viewCount",0)),"videos":int(c["statistics"].get("videoCount",0))}
def save():
    d=stats()
    json.dump(d,open(os.path.join(ROOT,"memory","channel_real.json"),"w"),ensure_ascii=False,indent=2)
    return d
if __name__=="__main__":
    print(save())
