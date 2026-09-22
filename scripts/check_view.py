import sys, json, time
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
SVC = get_authenticated_service()
def stats(vid):
	r = SVC.videos().list(part="statistics,snippet", id=vid).execute()
	it = r["items"][0]
	return int(it["statistics"].get("viewCount", "0")), int(it["statistics"].get("likeCount", "0")), it["snippet"]["title"]
v, l, t = stats('eybQ5ZKotOY')
print('VIDEO eybQ5ZKotOY:', v, 'views', l, 'likes')
print('TITLE:', t.encode('ascii', 'replace').decode())
