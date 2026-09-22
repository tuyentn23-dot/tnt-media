# publish_long.py
import os, sys, pickle
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
TOKEN=os.path.join(ROOT,"token.pickle")
def svc():
    d=pickle.load(open(TOKEN,"rb"))
    if d and d.expired and d.refresh_token: d.refresh(Request())
    return build("youtube","v3",credentials=d)

def upload(path, title, desc, tags, thumb=None, privacy="public"):
    y=svc()
    body={"snippet":{"title":title[:100],"description":desc,"tags":tags,"categoryId":"10"},"status":{"privacyStatus":privacy,"selfDeclaredMadeForKids":False}}
    media=MediaFileUpload(path, chunksize=-1, resumable=True)
    req=y.videos().insert(part="snippet,status", body=body, media_body=media)
    resp=None
    while resp is None:
            st,resp=req.next_chunk()
    vid=resp["id"]
    if thumb and os.path.exists(thumb):
        try:
            y.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb)).execute()
        except Exception as e: print("thumb err",e)
    return vid

if __name__=="__main__":
    import json
    cfg=json.load(open("output/_longcfg.json",encoding="utf-8"))
    vid=upload(cfg["path"], cfg["title"], cfg["desc"], cfg["tags"], cfg.get("thumb"))
    print("PUBLISHED https://youtu.be/"+vid)
