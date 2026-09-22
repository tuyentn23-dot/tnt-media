import sys
sys.path.insert(0,'.')
from ops import video_health as vh
r=vh.check('output/_test_dark.mp4')
print('ok=', r['ok'], 'reasons=', r['reasons'])
print('metrics=', r['metrics'])
