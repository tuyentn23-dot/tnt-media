import sys, time
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
SVC = get_authenticated_service()
VIDS = ['eybQ5ZKotOY', 'aAYGoWL2ZMo']
for v in VIDS:
	r = SVC.videos().list(part="statistics,snippet", id=v).execute()
	it = r["items"][0]
	st = it["statistics"]
	print(v, st.get("viewCount", "0"), 'views |', it["snippet"]["title"].encode('ascii', 'replace').decode()[:50])
