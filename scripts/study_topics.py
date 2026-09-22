import sys
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
s = get_authenticated_service()
def study(name, q):
	try:
		r = s.search().list(part='snippet', q=q, type='video', order='viewCount', maxResults=4, videoDuration='short').execute()
		ids = [i['id']['videoId'] for i in r['items']]
		st = s.videos().list(part='statistics,contentDetails', id=','.join(ids)).execute()
		print('===', name)
		for it in st['items']:
			v = it['statistics'].get('viewCount', '0')
			d = it['contentDetails']['duration']
			print(v, d)
	except Exception as e:
		print(name, 'ERR', str(e)[:60])
study('FOOD', 'cooking recipe short')
study('SATISFYING', 'oddly satisfying')
study('MAGIC', 'magic trick short')
study('SPORT', 'football skill')
