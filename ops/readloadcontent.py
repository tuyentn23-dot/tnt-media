src = open('ops/channel_loader.py', encoding='utf-8').read()
i = src.find('def load_content')
j = src.find('def ', i+10)
body = src[i:j]
for k, line in enumerate(body.split(chr(10))):
	print(k, repr(line))
