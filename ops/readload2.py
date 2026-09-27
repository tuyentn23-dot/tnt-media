src = open('ops/channel_loader.py', encoding='utf-8').read()
i = src.find('def load_content')
j = src.find('def ', i+10)
body = src[i:j]
open('logs/_loadcontent.txt', 'w', encoding='utf-8').write(body)
print('written', len(body))
