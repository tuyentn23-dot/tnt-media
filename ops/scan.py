import os
KEY='.with_'
def scan(root):
    res=[]
    for dp,dn,fn in os.walk(root):
        if 'pycache' in dp:
            continue
        for x in fn:
            if not x.endswith('.py'):
                continue
            p=os.path.join(dp,x)
            c=open(p,encoding='utf-8',errors='replace').read().split(chr(10))
            h=[(i+1,l.strip()[:90]) for i,l in enumerate(c) if KEY in l]
            if h:
                res.append((p,len(h),h))
    return res
for p,n,h in scan('ops'):
    print(p,n)
    [print(' ',i,t) for i,t in h]
