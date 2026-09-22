import os, sys, io, urllib.request
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
d=os.path.join('projects','art_doc','assets')
os.makedirs(d, exist_ok=True)
url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/1280px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg'
req=urllib.request.Request(url, headers={"User-Agent":"TNTMedia/1.0 (research)"})
data=urllib.request.urlopen(req, timeout=60).read()
p=os.path.join(d,'mona_lisa.jpg')
open(p,'wb').write(data)
print('ok', len(data), p)
