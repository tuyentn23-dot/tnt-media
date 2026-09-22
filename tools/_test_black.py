import sys
sys.path.insert(0,'.')
from ops import video_health as vh
r=vh.check('output/_test_black.mp4')
print('black video ok=', r['ok'])
print('reasons=', r['reasons'])
print('metrics=', r['metrics'])
