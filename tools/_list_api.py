import re
s=open('os_app/router.py',encoding='utf-8').read()
out=[]
for m in re.finditer(r'@router\.(get|post)\("([^"]+)"\)', s):
    out.append(m.group(1).upper()+' '+m.group(2))
for l in out:
    print(l.encode('ascii','replace').decode('ascii'))
