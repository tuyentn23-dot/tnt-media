import pickle, sys, os, time
sys.path.insert(0,'.')
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(os.getcwd(),'tools','ffmpeg.exe')
from googleapiclient.discovery import build
from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish

CID='Mialinhcute'
# 1) xoa video den tren YouTube
import pickle as pk
cfg=ch.load(CID)
tp=ch.token_path(cfg)
creds=pk.load(open(tp,'rb'))
from google.auth.transport.requests import Request
if not creds.valid and creds.refresh_token:
    creds.refresh(Request())
yt=build('youtube','v3',credentials=creds)
for vid in ['wZWEtIxwxlQ']:
    try:
        yt.videos().delete(id=vid).execute()
        print('deleted', vid)
    except Exception as e:
        print('del err', vid, str(e)[:120])

# 2) xoa sig meme_funny_dog_1 khoi ledger
import json, io
ledp='channels/'+CID+'/published_ledger.json'
led=json.load(io.open(ledp,encoding='utf-8'))
for s in list(led.get('signatures',{}).keys()):
    if 'meme_funny_dog_1' in s:
        del led['signatures'][s]
        print('removed sig', s[:40])
json.dump(led, io.open(ledp,'w',encoding='utf-8'), ensure_ascii=False, indent=2)

# 3) build lai + dang
cf.set_channel(CID)
os_publish.set_channel(CID)
style=cfg.get('style',{})
item=[it for it in ch.load_content(CID,'meme') if it['id']=='meme_funny_dog_1'][0]
out=os.path.abspath('output/ch'+CID+'_'+item['id']+'_'+time.strftime('%Y%m%d_%H%M%S')+'.mp4')
cs.build_styled(item, out, style=style)
print('built', out, os.path.getsize(out))
c=cfg.get('content',{})
title=item['hook'][:100]
desc=(item.get('body','')+' '+item.get('payoff',''))[:450]
tags=list(c.get('tags_base',[]))+[item.get('topic',''),CID]
topic='ch'+CID+'_meme_'+item['id']
res=os_publish.publish(out, title, description=desc, tags=tags, privacy='public', topic=topic, category_id=str(c.get('category_id','24')), force=True)
print('published', res)
if isinstance(res,dict) and res.get('ok'):
    cf.mark_published(cf.signature(item,'meme'), {'youtube_id': res.get('youtube_id'), 'topic': topic, 'kind':'meme', 'file': out})
    print('marked')
