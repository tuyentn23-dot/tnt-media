import requests
prompt = 'anime girl, pink hair, cute, masterpiece, best quality'
url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(prompt) + '?width=512&height=512&nologo=true&model=flux'
print('url:', url[:120])
try:
	r = requests.get(url, timeout=60)
	print('status:', r.status_code)
	print('ct:', r.headers.get('content-type'))
	print('bytes:', len(r.content))
	if r.status_code == 200 and len(r.content) > 5000:
		open('output/ai_test_01.jpg', 'wb').write(r.content)
		print('saved')
except Exception as e:
	print('ERR:', str(e)[:200])