import io
NL=chr(10)
add = [
'',
'## DA KENH + DASHBOARD (2026-09-19 cap nhat)',
'- Kenh quan ly: Mialinhcute (anime/roblox/cute_animals/meme), vilevi5676 (lifestyle/food/animals/nostalgia/curiosity, 16:9), whatif_vi',
'- Moi kenh co channels/<id>/channel.json + content_db.json + topic_pool.json + published_ledger.json + token.pickle',
'- Vile token: config/token.pickle (ViLe Vi UCbblZzHm3CZzmoUZznfIoTg)',
'- API: GET /os/api/channels ; POST /os/api/channels/{id}/toggle ; GET /os/api/channels/{id}/content',
'- Dashboard tab Channels: bang kenh, ON/OFF, kinds, video moi, da dang, nut bat/tat',
'- Caption nang cap: chu 44px, dat thap 0.68H, khong che hinh (channel_style.py)',
'- Batch: tools/batch_mia_v2.py, tools/batch_vile.py',
'- module moi: ops/mia_content.py (quan ly chu de moi + meme + chong lap)',
'- Meme topics: funny_cat_fail, funny_dog, satisfying_slime',
]
P='MEMORY.md'
s=io.open(P,encoding='utf-8').read()
s=s.rstrip()+NL+NL.join(add)+NL
io.open(P,'w',encoding='utf-8').write(s)
print('memory updated')
