import os, sys, pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
r=y.search().list(part="snippet",forMine=True,type="video",maxResults=25,order="date").execute()
for i in r.get("items",[]):
 print(i["id"]["videoId"],i["snippet"]["title"][:60])
