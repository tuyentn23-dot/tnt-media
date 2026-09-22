import os, sys, time, json, io, pickle
sys.path.insert(0,'.')
os.environ['IMAGEIO_FFMPEG_EXE']=os.path.join(os.getcwd(),'tools','ffmpeg.exe')
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish
CID='vilevi5676'
cfg=ch.load(CID)
tp=ch.token_path(cfg)
creds=pickle.load(open(tp,'rb'))
if not creds.valid and creds.refresh_token:
    creds.refresh(Request())
yt=build('youtube','v3',credentials=creds)
old=['j_XuSsdOxTc','7_7bZS2mkno','WiDC9YPPR6M']
for vid in old:
    try:
        yt.videos().delete(id=vid).execute()
        print('deleted', vid)
    except Exception as e:
        print('del err', vid, str(e)[:80])
# reset ledger
ledp='channels/'+CID+'/published_ledger.json'
json.dump({'signatures':{}}, io.open(ledp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('ledger reset')
# build + publish fresh
cf.set_channel(CID)
os_publish.set_channel(CID)
style=cfg.get('style',{})
for kind in cfg.get('content',{}).get('kinds',[]):
    items=ch.load_content(CID,kind)
    fresh=[it for it in items if not cf.is_published(cf.signature(it,kind))]
    if not fresh: continue
    item=fresh[0]
    out=os.path.abspath('output/ch'+CID+'_'+item['id']+'_'+time.strftime('%Y%m%d_%H%M%S')+'.mp4')
    cs.build_styled(item, out, style=style)
    sz=os.path.getsize(out)
    print('built', item['id'], sz)
    if sz < 500000:
        print('SKIP small'); continue
    c=cfg.get('content',{})
    title=item['hook'][:100]
    desc=(item.get('body','')+' '+item.get('payoff',''))[:450]
    tags=list(c.get('tags_base',[]))+[item.get('topic',''),CID]
    topic='ch'+CID+'_'+kind+'_'+item['id']
    res=os_publish.publish(out, title, description=desc, tags=tags, privacy='public', topic=topic, category_id=str(c.get('category_id','22')), force=True)
    print('pub', item['id'], res.get('youtube_id') if isinstance(res,dict) else res)
    if isinstance(res,dict) and res.get('ok'):
        cf.mark_published(cf.signature(item,kind), {'youtube_id': res.get('youtube_id'), 'topic': topic, 'kind': kind, 'file': out})
