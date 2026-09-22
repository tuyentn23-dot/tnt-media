import os, sys, json
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.http
TOKEN = 'memory/token.json'
VIDEO = os.path.abspath(os.path.join('output', 'CHECK', 'gacha_clip.mp4'))
print('video exists:', os.path.exists(VIDEO), os.path.getsize(VIDEO))
creds = google.oauth2.credentials.Credentials.from_authorized_user_file(TOKEN)
print('scopes:', creds.scopes)
yt = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
title = 'Gacha Anime Test - Skeleton + Bezier'
desc = 'Test clip: anime gacha voi skeleton + bezier path + nhac Suno.'
body = {
	'snippet': {
		'title': title,
		'description': desc,
		'tags': ['gacha', 'anime', 'shorts'],
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
while resp is None:
	st, resp = req.next_chunk()
	if st:
		print('progress', int(st.progress() * 100), '%')
print('video id:', resp['id'])
print('URL: https://youtu.be/' + resp['id'])