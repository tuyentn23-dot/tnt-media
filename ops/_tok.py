import sys,os,pickle
sys.path.insert(0,os.getcwd())
from ops import channel_loader as ch
def chk(cid):
    try:
        cfg=ch.load(cid)
        tp=ch.token_path(cfg)
        c=pickle.load(open(tp,'rb'))
        v=getattr(c,'valid',None)
        e=getattr(c,'expired',None)
        s=len(getattr(c,'scopes',[]) or [])
        print(cid, v, e, s)
    except Exception as ex:
        print(cid, 'ERR', repr(ex))
chk('Mialinhcute')
chk('vilevi5676')
