# -*- coding: utf-8 -*-
import io, base64
P='os_app/ui/index.html'
s=io.open(P,encoding='utf-8',errors='replace').read()
js=base64.b64decode(open('tools/_agent_js.b64').read().strip()).decode('utf-8')
# 1) add tab before videos
old="['videos','Video','VID','Thu vien video'],"
new="['agent','Agent','BOT','Mo web - chup man hinh - lenh'],"+old
if "'agent'" not in s[:7000]:
    s=s.replace(old,new,1); print('tab added')
else:
    print('tab exists')
# 2) add function before videos
marker='async function videos()'
if 'async function agent()' not in s:
    s=s.replace(marker, js+chr(10)+marker, 1); print('fn added')
else:
    print('fn exists')
# 3) register renderer
oldm='{dashboard:dash,videos:videos,'
newm='{dashboard:dash,agent:agent,videos:videos,'
if oldm in s:
    s=s.replace(oldm,newm,1); print('renderer registered')
else:
    print('map not found')
io.open(P,'w',encoding='utf-8').write(s)
print('written', len(s))
