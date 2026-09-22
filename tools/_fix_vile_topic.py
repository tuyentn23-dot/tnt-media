import json, io
P='channels/vilevi5676/content_db.json'
d=json.load(io.open(P,encoding='utf-8'))
# topic phai tro dung folder footage: lifestyle/food/animals/nostalgia/curiosity
fix={'life_morning_1':'lifestyle','food_pho_1':'food','animal_dolphin_1':'animals','nost_90s_1':'nostalgia','cur_why_sky_1':'curiosity'}
for k,items in d.items():
    for it in items:
        if it['id'] in fix:
            it['topic']=fix[it['id']]
json.dump(d, io.open(P,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
for k,items in d.items():
    print(k, [(it['id'], it['topic']) for it in items])
