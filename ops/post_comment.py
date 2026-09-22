import pickle, json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
cm=json.load(open("output/_cmcfg.json",encoding="utf-8"))
body={"snippet":{"videoId":cm["vid"],"topLevelComment":{"snippet":{"textOriginal":cm["text"]}}}}
r=y.commentThreads().insert(part="snippet",body=body).execute()
print("COMMENTED "+r["id"])
