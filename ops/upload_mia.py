import os, sys
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.http
TOKEN = 'memory/token_new_channel.json'
VIDEO = os.path.abspath(os.path.join('output', 'CHECK', 'gacha_clip.mp4'))
print('video:', os.path.getsize(VIDEO), 'bytes')
creds = google.oauth2.credentials.Credentials.from_authorized_user_file(TOKEN)
yt = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
body = {
	'snippet': {
		'title': 'Gacha Anime Test - Skeleton + Bezier',
		'description': 'Test clip: anime gacha voi skeleton + bezier path + nhac Suno.',
		'tags': ['gacha', 'anime', 'shorts', 'mia linh cute'],
		'categoryId': '24'
	},
	'status': {
		'privacyStatus': 'private',
		'selfDeclaredMadeForKids': False
	}
}
media = googleapiclient.http.MediaFileUpload(VIDEO, chunksize=-1, resumable=True, mimetype='video/mp4')
req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
resp = None
import time
t0 = time.time()
while resp is None:
	st, resp = req.next_chunk()
	if st:
		print('progress', int(st.progress() * 100), '%', round(time.time() - t0, 1), 's')
print('uploaded id:', resp['id'])
print('URL: https://youtu.be/' + resp['id'])