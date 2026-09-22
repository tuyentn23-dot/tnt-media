s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
# tim cac doan co the gay loi JS: 'mc PdXQ', hay ky tu la
import re
bad=[]
for kw in ['mc PdXQ','undefined',']]]',')))}','<div class=grid']:
    if kw in s:
        bad.append(kw)
print('suspicious:', bad)
# in 200 ky tu quanh ham agent va videos
i=s.find('async function agent()')
print('--- agent ---')
print(s[i:i+300].encode('ascii','replace').decode('ascii'))
j=s.find('async function videos()')
print('--- videos ---')
print(s[j:j+300].encode('ascii','replace').decode('ascii'))
