import io, os, json
p = 'channels/Mialinhcute/channel.json'
cfg = json.load(io.open(p, encoding='utf-8'))
cfg['name'] = 'Mia Linh Cute'
cfg['enabled'] = False
cfg['token_file'] = 'token.pickle'
cfg['style'] = {
	'language': 'vi',
	'voice': 'female_cute',
	'music_genre': 'happy_kids',
	'color_primary': '#ff69b4',
	'color_accent': '#ffd700',
	'font': 'Arial-Bold',
	'font_size': 78,
	'watermark': '@Mialinhcute',
	'intro_seconds': 0.5,
	'outro_seconds': 1.0,
	'aspect': '9:16',
	'max_duration_sec': 50,
}
cfg['content'] = {
	'kinds': ['anime', 'roblox', 'cute_animals'],
	'category_id': '24',
	'tags_base': ['shorts', 'forkids', 'kids', 'viral', 'cutecute'],
	'title_template': '{hook}',
	'desc_template': '{body} {payoff}',
	'topic_pool_file': 'topic_pool.json',
}
cfg['schedule'] = {
	'enabled': True,
	'interval_min': 90,
	'batch': 2,
	'post_hours': [7, 11, 16, 19, 21],
}
io.open(p, 'w', encoding='utf-8').write(json.dumps(cfg, ensure_ascii=False, indent=2))

content = {
	'anime': [
		{'id': 'anime_doraemon', 'topic': 'doraemon', 'hook': 'Doraemon co that su co that khong?', 'body': 'Doraemon la chu meo may den tu tuong lai the ky 22. Nhung ban co biet, tac gia da lay cam hung tu mot chu meo that bi mat tich?', 'payoff': 'Chu meo do ten la Chibi, va no da thay doi ca su nghiep cua tac gia!', 'question': 'Ban thich nhan vat nao nhat?'},
		{'id': 'anime_conan', 'topic': 'conan', 'hook': 'Conan da pha bao nhieu vu an?', 'body': 'Shinichi Kudo bi thuoc teo nho thanh Conan. Tren 1000 chuong truyen, cau da pha hon 300 vu an.', 'payoff': 'Nhung vu an kho nhat lai lien quan den to chuc Ao Den!', 'question': 'Ban doan ket cuoi the nao?'},
	],
	'roblox': [
		{'id': 'roblox_adooptme', 'topic': 'adoptme', 'hook': 'Meo trong Adopt Me dat nhat bao nhieu?', 'body': 'Trong Roblox Adopt Me, co nhung con pet cuc hiem. Meo Shadow Dragon la mot trong so do.', 'payoff': 'Co nguoi tra gia no bang ca thang luong!', 'question': 'Ban co pet nao hiem nhat?'},
		{'id': 'roblox_brookhaven', 'topic': 'brookhaven', 'hook': 'Brookhaven co bao nhieu ngoi nha?', 'body': 'Brookhaven la thanh pho lon nhat Roblox voi hang tram ngoi nha va bi mat.', 'payoff': 'Co mot ngoi nha an khong hien tren ban do!', 'question': 'Ban da tim thay chua?'},
	],
	'cute_animals': [
		{'id': 'animal_capybara', 'topic': 'capybara', 'hook': 'Tai sao capybara than thien voi moi loai?', 'body': 'Capybara la dong vat than thien nhat the gioi. Chung co the ket ban voi ca ca sau.', 'payoff': 'Ly do la chung co mot mui huong dac biet khien moi loai deu thich!', 'question': 'Ban co muon nuoi capybara khong?'},
		{'id': 'animal_redpanda', 'topic': 'redpanda', 'hook': 'Gau truc do co phai gau truc khong?', 'body': 'Red panda khong phai gau truc. No thuoc ho rieng, gan voi chon va raccoon hon.', 'payoff': 'Nhung nguoi ta van goi no la gau truc do vi qua de thuong!', 'question': 'Ban thay no de thuong khong?'},
	],
}
io.open('channels/Mialinhcute/content_db.json', 'w', encoding='utf-8').write(json.dumps(content, ensure_ascii=False, indent=2))

pool = {
	'anime': ['naruto', 'onepiece', 'dragonball', 'pokemon', 'sailormoon'],
	'roblox': ['piggy', 'arsenal', 'bloxfruits', 'jailbreak', 'mm2'],
	'cute_animals': ['shiba', 'panda', 'axolotl', 'quokka', 'fennec'],
}
io.open('channels/Mialinhcute/topic_pool.json', 'w', encoding='utf-8').write(json.dumps(pool, ensure_ascii=False, indent=2))
print('MIALINHCUTE SETUP DONE')
for k in content:
	print(' ', k, '=', len(content[k]), 'items')
