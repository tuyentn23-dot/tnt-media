# -*- coding: utf-8 -*-
import json
p = 'channels/Mialinhcute/content_db.json'
d = json.load(open(p, encoding='utf-8'))
new = {
 'anime': [{
   'id': 'anime_pokemon',
   'topic': 'pokemon',
   'hook': 'Pikachu có thực sự là chuột?',
   'body': 'Pikachu được lấy cảm hứng từ loài chuột pika nhỏ bá. Nhưng nó lại có đang điện mạnh đến mức hạ gục cạ thỏ tƸn lớn.',
   'payoff': 'Hóa ra chuột nhỏ cũng có thể trở thành huyền thoại!',
   'question': 'Bạn chọn Pikachu yam Eevee?'
 }],
 'roblox': [{
   'id': 'roblox_adoptme_2',
   'topic': 'adoptme',
   'hook': 'Bí mật thú cúng hiếm trong Adopt Me',
   'body': 'Trong Adopt Me có những thú cúng chệ xuất hiện một lần trong sự kiện đặc biệt. Người chơi phải đǡi hàng năm mới có cơ hội sở hữu.',
   'payoff': 'Có người đã đợi 3 năm chỉ để có một chuột mèo hiắm!',
   'question': 'Bạn tng sở hứu thú cúng hiếm nào?'
 }],
 'cute_animals': [{
   'id': 'animal_shiba',
   'topic': 'shiba',
  'hook': 'Shiba Inu cười thực sự nghĩa là gì?',
   'body': 'Shiba Inu là giống chó nhỏ nhất của Nhật Bản, có xinh thực là chó nhỏ buụi riại. Nhưng tiếng cười của nó lại là một đặc trưng quý hiếm.',
   'payoff': 'Nười Nhật coi tiếng cười của Shiba là biểu tượng của niềm vui!',
   'question': 'Bạn thấy Shiba dễ thương không?'
 }],
}
for k, items in new.items():
    ids = [it['id'] for it in d.get(k, [])]
    for it in items:
        if it['id'] not in ids:
            d.setdefault(k, []).append(it)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('total', {k: len(v) for k, v in d.items()})
