parts=['_c1.html','_c2.html','_c3.html','_c4.html','_c5.html','_c6.html','_c7.html']
out=''
for p in parts:
    out+=open('tools/'+p,encoding='utf-8').read()
open('os_app/ui/control.html','w',encoding='utf-8').write(out)
print('control.html size', len(out))
