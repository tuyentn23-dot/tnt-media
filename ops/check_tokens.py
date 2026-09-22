import json
files = ['memory/token_new_channel.json', 'memory/token.json', 'memory/token_channel_01.json', 'memory/token_channel_02.json']
for fn in files:
	try:
		d = json.load(open(fn, encoding='utf-8'))
		print('===', fn)
		print(' scopes:', d.get('scopes'))
		print(' has refresh:', bool(d.get('refresh_token')))
		print(' client_id:', str(d.get('client_id', ''))[:40])
	except Exception as e:
		print(fn, 'ERR', e)