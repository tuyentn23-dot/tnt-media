import sys
sys.path.insert(0,'.')
from ops import video_health as vh
for v in ['output/_test_black2.mp4']:
    r=vh.check(v)
    print(v, 'ok=', r['ok'], 'reasons=', r['reasons'])
    print('  metrics=', r['metrics'])
