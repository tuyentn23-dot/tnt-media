import pickle, json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
cfg=json.load(open("output/_seo_update.json",encoding="utf-8"))
vid=cfg.pop("id")
body={"id":vid,"snippet":cfg}
y.videos().update(part="snippet",body=body).execute()
print("UPDATED "+vid)
