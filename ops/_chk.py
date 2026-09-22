import sys,os
sys.path.insert(0,os.getcwd())
from ops import channel_loader as ch
def go(cid):
    try:
        cfg=ch.load(cid)
        tp=ch.token_path(cfg)
        ok=os.path.exists(tp) if tp else False
        print(cid, cfg.get('name'), tp, ok)
    except Exception as e:
        print(cid, 'ERR', repr(e))
print('list', ch.list_channels())
go('Mialinhcute')
go('vilevi5676')
