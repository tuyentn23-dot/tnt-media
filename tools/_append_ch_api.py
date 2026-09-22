api=open('tools/_ch_api.txt',encoding='utf-8').read()
P='os_app/router.py'
s=open(P,encoding='utf-8').read()
mark='def auto_publish(topic: str, hook'
i=s.find(mark)
# append at end of file instead (after last function)
s2=s.rstrip()+chr(10)+api
open(P,'w',encoding='utf-8').write(s2)
print('appended, new len', len(s2))
