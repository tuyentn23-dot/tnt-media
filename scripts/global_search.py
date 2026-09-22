import sys, json
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
s = get_authenticated_service()
q = 'cat shorts'
r = s.search().list(part='snippet', q=q, type='video', order='viewCount', maxResults=10, videoDuration='short').execute()
for it in r['items']:
	print(it['snippet']['channelTitle'].encode('ascii', 'replace').decode(), '|', it['snippet']['title'].encode('ascii', 'replace').decode()[:50])
