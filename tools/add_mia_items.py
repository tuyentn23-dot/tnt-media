# -- coding: utf-8 --
import json, os
p = 'channels/Mialinhcute/content_db.json'
d = json.load(open(p, encoding='utf-8'))
new = {
 'anime': [{
 'id': 'anime_pokemon',
 'topic': 'pokemon',
 'hook': 'Pikachu co thuc su la chuot?',
 'body': 'Pikachu duoc lay cam hung tu loai chuot pika nho be. Nhung no lai co dong dien manh den muc ha guc ca doi thu to lon.',
 'payoff': 'Hoa ra chuot nho cung co the tro thanh huyen thoai!',
 'question': 'Ban chon Pikachu hay Eevee?'
 }],
 'roblox': [{
 'id': 'roblox_adoptme_2',
 'topic': 'adoptme',
 'hook': 'Bi mat thu cung hiem trong Adopt Me',
 'body': 'Trong Adopt Me co nhung thu cung chi xuat hien mot lan trong su kien dac biet. Nguoi choi phai doi hang nam moi co co hoi so huu.',
 'payoff': 'Co nguoi da doi 3 nam chi de co mot chu meo hiem!',
 'question': 'Ban tung so huu thu cung hiem nao?'
 }],
 'cute_animals': [{
 'id': 'animal_shiba',
 'topic': 'shiba',
 'hook': 'Shiba Inu cuoi that su nghia la gi?',
 'body': 'Shiba Inu la giong cho nho nhat cua Nhat Ban, co nghia la cho nho bui roi. Nhung tieng cuoi cua no lai la mot dac trung quy hiem.',
 'payoff': 'Nguoi Nhat coi tieng cuoi cua Shiba la bieu tuong cua niem vui!',
 'question': 'Ban thay Shiba de thuong khong?'
 }],
}
for k, items in new.items():
 ids = [it['id'] for it in d.get(k, [])]
 for it in items:
 if it['id'] not in ids:
 d.setdefault(k, []).append(it)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('added items', [it['id'] for it in new.get('anime',[]) + new.get('roblox',[]) + new.get('cute_animals',[])])
print('total', {k: len(v) for k, v in d.items()})
