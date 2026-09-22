# -- coding: utf-8 --
import sys, os, json, base64
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.getcwd())
from ops.os_publish import publish

b = open('output/seo_payload.b64').read().strip()
payload = json.loads(base64.b64decode(b).decode('utf-8'))

video = os.path.join('output', 'seo_test_video.mp4')
res = publish(video, payload['title'], description=payload['desc'], tags=payload['tags'], privacy='public', topic='beauty_antiaging')
print(json.dumps(res, ensure_ascii=False))
