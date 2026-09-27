import sys, os, pickle
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from googleapiclient.discovery import build
TOK = {'Mialinhcute': 'channels/Mialinhcute/token.pickle', 'whatif_vi': 'channels/whatif_vi/token.pickle', 'vilevi5676': 'config/token.pickle'}
def who(ch, tp):
	try:
		creds = pickle.load(open(tp, 'rb'))
		yt = build('youtube', 'v3', credentials=creds)
		r = yt.channels().list(part='snippet', mine=True).execute()
		items = r.get('items', [])
		return (ch, items[0]['snippet']['title'] if items else 'NO CHANNEL')
	except Exception as e:
		return (ch, 'ERR ' + str(e)[:90])
for ch, tp in TOK.items():
	print(who(ch, tp))
