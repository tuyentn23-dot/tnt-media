import os
KEY='.with_'
def go(root):
    res=[]
    for dp,dn,fn in os.walk(root):
        if 'pycache' in dp:
            continue
        for x in fn:
            if not x.endswith('.py'):
                continue
            p=os.path.join(dp,x)
            c=open(p,encoding='utf-8',errors='replace').read()
            n=c.count(KEY)
            if n>0:
                res.append((p,n))
    return res
[print(p,n) for p,n in go('ops')]
