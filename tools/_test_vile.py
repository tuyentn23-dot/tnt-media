import os, sys, time
sys.path.insert(0,'.')
os.environ['IMAGEIO_FFMPEG_EXE']=os.path.join(os.getcwd(),'tools','ffmpeg.exe')
from ops import channel_loader as ch
from ops import channel_style as cs
CID='vilevi5676'
cfg=ch.load(CID)
style=cfg.get('style',{})
item=ch.load_content(CID,'lifestyle')[0]
print('item topic:', item['topic'])
out=os.path.abspath('output/_test_vile_'+time.strftime('%H%M%S')+'.mp4')
cs.build_styled(item, out, style=style)
print('built', out, os.path.getsize(out))
