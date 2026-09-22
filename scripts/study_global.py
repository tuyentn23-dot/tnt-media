import sys, json
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
s = get_authenticated_service()
def study(name, q):
	r = s.search().list(part='snippet', q=q, type='video', order='viewCount', maxResults=5, videoDuration='short').execute()
	ids = [i['id']['videoId'] for i in r['items']]
	st = s.videos().list(part='statistics,snippet,contentDetails', id=','.join(ids)).execute()
	print('===', name)
	for it in st['items']:
		v = it['statistics'].get('viewCount', '0')
		d = it['contentDetails']['duration']
		t = it['snippet']['title'].encode('ascii', 'replace').decode()[:45]
		print(v, d, t)
study('CAT GLOBAL', 'cute cat funny')
study('DOG GLOBAL', 'funny dog')
