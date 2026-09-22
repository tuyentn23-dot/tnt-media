import os, sys, time
sys.path.insert(0, '.')
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe')
from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish

CID='Mialinhcute'
cfg=ch.load(CID)
style=cfg.get('style',{})
cf.set_channel(CID)
os_publish.set_channel(CID)

# rebuild + publish 2 meme fresh
items=[it for it in ch.load_content(CID,'meme') if not cf.is_published(cf.signature(it,'meme'))][:2]
print('fresh memes:', [it['id'] for it in items])
for item in items:
    out=os.path.abspath('output/ch'+CID+'_'+item['id']+'_'+time.strftime('%Y%m%d_%H%M%S')+'.mp4')
    cs.build_styled(item, out, style=style)
    sz=os.path.getsize(out)
    print('built', out, sz)
    if sz > 500000:
        c=cfg.get('content',{})
        title=item['hook'][:100]
        desc=(item.get('body','')+' '+item.get('payoff',''))[:450]
        tags=list(c.get('tags_base',[]))+[item.get('topic',''),CID]
        topic='ch'+CID+'_meme_'+item['id']
        res=os_publish.publish(out, title, description=desc, tags=tags, privacy='public', topic=topic, category_id=str(c.get('category_id','24')), force=True)
        print('published', res)
        if isinstance(res, dict) and res.get('ok'):
            cf.mark_published(cf.signature(item,'meme'), {'youtube_id': res.get('youtube_id'), 'topic': topic, 'kind':'meme', 'file': out})
            print('marked')
