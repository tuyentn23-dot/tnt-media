# -- coding: utf-8 --
import os, sys, io, json, time
sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from ops import art_doc as ad

t = time.time()
sc = ad.write_script('Mona Lisa', 'Mona Lisa cua Leonardo da Vinci, bao tang Louvre, nu cuoi bi an.', sections=2)
open('projects/art_doc/_test_script2.json', 'w', encoding='utf-8').write(json.dumps({'sc': sc, 'time': round(time.time()-t,1)}, ensure_ascii=False, indent=2))
print('DONE', round(time.time()-t,1))
