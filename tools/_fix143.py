P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
# Dòng 143 sai: src=\"\"+v.url+\"\"  -> đúng phải là src="+v.url+"
# Trong file HTML thực, chuỗi là: <video src=\"\"+v.url+\"\" preload=metadata muted>
import re
before=s.count('src=\\"\\"+v.url+\\"\\"')
print('occurrences of bad src:', before)
s=s.replace('src=\\"\\"+v.url+\\"\\"','src="+v.url+"')
open(P,'w',encoding='utf-8').write(s)
print('done')
