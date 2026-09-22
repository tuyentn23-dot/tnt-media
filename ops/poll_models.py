import requests
for u in ['https://image.pollinations.ai/models', 'https://image.pollinations.ai/']:
	try:
		r = requests.get(u, timeout=20)
		print(u, '->', r.status_code, r.text[:400])
	except Exception as e:
		print(u, 'ERR', str(e)[:100])