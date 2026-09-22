import os, sys, time
sys.path.insert(0,'.')
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(os.getcwd(),'tools','ffmpeg.exe')
from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish
CID='Mialinhcute'
cfg=ch.load(CID)
style=cfg.get('style',{})
cf.set_channel(CID)
os_publish.set_channel(CID)
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
print('pub', res.get('youtube_id') if isinstance(res,dict) else res)
if isinstance(res,dict) and res.get('ok'):
    cf.mark_published(cf.signature(item,'meme'), {'youtube_id': res.get('youtube_id'), 'topic': topic, 'kind':'meme', 'file': out})
    print('marked')
