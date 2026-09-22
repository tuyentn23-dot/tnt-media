import sys, json
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
s = get_authenticated_service()
ch = s.channels().list(part='contentDetails', mine=True).execute()
up = ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']
allv = []
tok = None
while True:
	pl = s.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
	items = pl['items']
	for i in items:
		allv.append(i['contentDetails']['videoId'])
	tok = pl.get('pageToken')
	if not tok:
		break
print('TOTAL:', len(allv))
rows = []
for i in range(0, len(allv), 50):
	chunk = allv[i:i+50]
	st = s.videos().list(part='snippet,statistics,contentDetails', id=','.join(chunk)).execute()
	for it in st['items']:
		rows.append({'id': it['id'], 'title': it['snippet']['title'], 'pub': it['snippet']['publishedAt'], 'dur': it['contentDetails']['duration'], 'views': int(it['statistics'].get('viewCount', '0')), 'likes': int(it['statistics'].get('likeCount', '0')), 'cmts': int(it['statistics'].get('commentCount', '0'))})
json.dump(rows, open('analytics/all_videos.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('SAVED', len(rows))
