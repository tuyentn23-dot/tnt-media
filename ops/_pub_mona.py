import os, sys, io, json
sys.path.insert(0, os.path.abspath('.'))
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
from ops import os_publish
v=os.path.join('output','artdocmona_lisa20260918101120.mp4')
title='Mona Lisa: Nụ Cười Bí Ẩn Và Những Câu Chuyện Ly Kỳ Chưa Kể'
desc='Soi kỹ bức tranh nổi tiếng nhất thế giới - Mona Lisa của Leonardo da Vinci. Những bí mật, câu chuyện ly kỳ và sự thật ít ai biết. #art #documentary'
res=os_publish.publish(v,title,description=desc,tags=['mona lisa','hoi hoa','nghe thuat','documentary'],privacy='public',topic='artdoc_mona_lisa',category_id='27',force=True)
print(json.dumps(res,ensure_ascii=False,default=str))
