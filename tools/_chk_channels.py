import sys, json
sys.path.insert(0,'.')
from ops import channel_loader as ch
from ops import content_freshness as cf
out=[]
for cid in ch.list_channels():
    try:
        cfg=ch.load(cid)
    except Exception as e:
        out.append({'id':cid,'error':str(e)}); continue
    cf.set_channel(cid)
    kinds=cfg.get('content',{}).get('kinds',[])
    fresh={}
    for k in kinds:
        items=ch.load_content(cid,k)
        fresh[k]=len([it for it in items if not cf.is_published(cf.signature(it,k))])
    out.append({'id':cid,'enabled':cfg.get('enabled'),'kinds':kinds,'fresh':fresh,'published':cf.published_count()})
print(json.dumps(out, ensure_ascii=True))
