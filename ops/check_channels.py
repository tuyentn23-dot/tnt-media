import os, sys
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.http
VIDEO = os.path.abspath(os.path.join('output', 'CHECK', 'gacha_clip.mp4'))
for TOKEN in ['memory/token_new_channel.json', 'memory/token_channel_01.json', 'memory/token_channel_02.json']:
	try:
		creds = google.oauth2.credentials.Credentials.from_authorized_user_file(TOKEN)
		yt = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
		# chi lay channel info truoc de test token
		r = yt.channels().list(part='snippet', mine=True).execute()
		items = r.get('items', [])
		if items:
			print(TOKEN, '->', items[0]['snippet']['title'], items[0]['id'])
		else:
			print(TOKEN, '-> no channel')
	except Exception as e:
		print(TOKEN, 'ERR:', str(e)[:100])