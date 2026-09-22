import json
p='config/scripts_vi.json'
d=json.load(open(p,encoding='utf-8'))
new={'anime':{'hook':'The Gioi Anime','lines':['The gioi anime day mau sac va phieu luu.','Moi nhan vat deu co mot uoc mo that dep.','Tu tinh ban den long dung cam, tat ca deu truyen cam hung.','Hay cung kham pha nhung cau chuyen tuyet voi nhe!']},
'roblox':{'hook':'The Gioi Roblox','lines':['Roblox la the gioi sang tao khong gioi han.','Ban co the xay nha, choi game va ket ban.','Moi tro choi la mot cuoc phieu luu moi.','Hay cung nhau kham pha va sang tao nhe!']},
'cute_animals':{'hook':'Nhung Ban Thu Cute','lines':['Nhung chu thu nho dang yeu luon lam ta vui.','Chung co bo long mem va doi mat tron xoe.','Moi cu chi deu dang yeu het muc.','Hay yeu thuong cac ban nho nay nhe!']},
'meme':{'hook':'Meme Vui Nhon','lines':['Meme mang lai tieng cuoi cho moi nguoi.','Chi can mot buc anh cung khien ta vui ca ngay.','Tien cuoi la lieu thuoc tinh than tuyet voi.','Hay chia se tieng cuoi den ban be nhe!']},
'gacha':{'hook':'The Gioi Gacha','lines':['Gacha la noi ban tao nhan vat cua rieng minh.','Moi nhan vat co kieu toc va trang phuc dep.','Ban co the ke nhung cau chuyen thu vi.','Hay cung nhau sang tao the gioi mo uoc nhe!']}}
for k,v in new.items():
    if k not in d:
        d[k]=v
        print('added', k)
    else:
        print('exists', k)
json.dump(d, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('total', len(d))
