import sys,os,pickle
sys.path.insert(0,os.getcwd())
from ops import channel_loader as ch
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
def chk(cid):
    try:
        cfg=ch.load(cid)
        tp=ch.token_path(cfg)
        c=pickle.load(open(tp,'rb'))
        if not c.valid and c.refresh_token:
            c.refresh(Request())
            pickle.dump(c, open(tp,'wb'))
        y=build('youtube','v3',credentials=c)
        r=y.channels().list(part='snippet',mine=True).execute()
        it=r.get('items',[])
        nm=it[0].get('snippet',{}).get('title') if it else 'NONE'
        print(cid, 'OK', str(nm).encode('ascii','replace').decode())
    except Exception as ex:
        print(cid, 'ERR', repr(ex)[:200])
chk('Mialinhcute')
chk('vilevi5676')
