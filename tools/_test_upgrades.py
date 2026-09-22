import sys, os
sys.path.insert(0,'.')
from ops import video_health as vh
# Test health check tren video cu (den) va video moi (co hinh)
for v in ['output/chMialinhcute_anime_doraemon_20260919_112544.mp4',
          'output/chMialinhcute_anime_dragonball_20260919_180306.mp4',
          'output/chvilevi5676_life_morning_1_20260919_195020.mp4']:
    if os.path.exists(v):
        r=vh.check(v)
        print(os.path.basename(v)[:50], 'ok=', r['ok'], 'reasons=', r['reasons'], 'mean=', r['metrics'].get('mean_avg'))
    else:
        print(v, 'MISSING')
