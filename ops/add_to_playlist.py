import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
y.playlistItems().insert(part="snippet",body={"snippet":{"playlistId":"PLXw2skh_HhUY","resourceId":{"kind":"youtube#video","videoId":"OQ_kcqi0euA"}}}).execute()
print("ADDED")
