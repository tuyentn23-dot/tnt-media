import base64
b=open('tools/_mia_content_b64.txt').read().strip()
t=base64.b64decode(b).decode('utf-8')
t=t.replace('abspath(file)','abspath(__file__)')
t=t.replace('# -- coding','# -*- coding')
open('ops/mia_content.py','w',encoding='utf-8').write(t)
print('OK')
