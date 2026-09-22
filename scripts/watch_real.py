import sys, time
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
s = get_authenticated_service()
v = 'X5Ic2a4eCig'
for i in range(6):
	r = s.videos().list(part="statistics,contentDetails,snippet", id=v).execute()
	it = r["items"][0]
	st = it["statistics"]
	print(i, st.get("viewCount", "0"), it["contentDetails"]["duration"])
	time.sleep(20)
