P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
# sua loi src\"\"+v.url+\"\" thanh src="+v.url+"
bad='<video src=\\"\\"+v.url+\\"\\" preload=metadata muted>'
good='<video src="+v.url+" preload=metadata muted>'
print('found bad:', bad in s)
s=s.replace(bad,good)
# cung sua class=\"\" trong cac chuoi khac neu co
open(P,'w',encoding='utf-8').write(s)
print('fixed')
# re-extract + validate
import subprocess
i=s.find('<script>')
j=s.rfind('</script>')
open('tools/_ui.js','w',encoding='utf-8').write(s[i+8:j])
print('re-extracted')
