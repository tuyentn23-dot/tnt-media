import pickle, json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
updates=json.load(open("output/_title_updates.json",encoding="utf-8"))
for u in updates:
 r=y.videos().list(part="snippet",id=u["id"]).execute()
 sn=r["items"][0]["snippet"]
 sn["title"]=u["title"]
 y.videos().update(part="snippet",body={"id":u["id"],"snippet":sn}).execute()
 print("OK "+u["id"])
