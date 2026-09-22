# comment_bot.py - read comments, auto-reply with smart responses
# NOTE: needs youtube.force-ssl scope (re-auth required)
import os,sys,json,pickle,random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

REPLIES = ["Cảm ơn bạn đã xem! Bạn nghĩ sao về điều này?", "Hay đấy! Theo dõi kênh để xem thêm nhé.", "Câu hỏi thú vị! Mình sẽ làm video về nó.", "Bạn đoán đúng rồi đấy!", "Cảm ơn bạn! Bạn muốn xem chủ đề gì tiếp?"]

def yt():
    d = pickle.load(open(os.path.join(ROOT,"token.pickle"),"rb"))
    if d and d.expired and d.refresh_token: d.refresh(Request())
    return build("youtube","v3",credentials=d)

def get_comments(video_id):
    y = yt()
    r = y.commentThreads().list(part="snippet",videoId=video_id,maxResults=20).execute()
    return [it["snippet"]["topLevelComment"] for it in r.get("items",[])]

def reply(comment_id, text):
    y = yt()
    y.comments().insert(part="snippet",body={"snippet":{"parentId":comment_id,"textOriginal":text}}).execute()
    return True

def auto_reply(video_id):
    out = []
    for c in get_comments(video_id):
        cid = c["id"]
        try:
            reply(cid, random.choice(REPLIES)); out.append(cid)
        except Exception as e:
            out.append("FAIL "+str(e)[:80])
    return out

if __name__ == "__main__":
    print("comment bot ready (needs force-ssl scope)")
