import os
hits=[]
for dp,dn,fn in os.walk('.'):
    if '.git' in dp or 'pycache' in dp:
        continue
    for f in fn:
        if f.lower().endswith(('.wav','.mp3','.m4a')):
            hits.append((os.path.getsize(os.path.join(dp,f)), os.path.join(dp,f)))
for s,p in sorted(hits):
    print(s, p)
