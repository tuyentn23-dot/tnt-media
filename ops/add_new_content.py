# -- coding: utf-8 --
import json, io, os
NL = chr(10)

NEW_MIA = {
	'gacha': [{
		'id': 'gacha_new_01', 'topic': 'gacha',
		'hook': 'Cô gái Gacha bỏ học vì gia đình nghèo',
		'body': 'Cô bé Gacha tên Linh phải nghỉ học để phụ mẹ bán hàng rong. Mỗi đêm, cô vẫn lén mở game Gacha để vẽ ước mơ của mình.',
		'payoff': 'Một ngày, ước mơ ấy thành sự thật theo cách không ai ngờ tới.',
		'search_query': 'gacha cute animation story'
	}],
	'anime': [{
		'id': 'anime_new_01', 'topic': 'anime',
		'hook': 'Naruto mạnh nhất khi nào?',
		'body': 'Naruto Uzumaki từ một đứa trẻ bị cả làng xa lánh đã trở thành Hokage. Sức mạnh thật sự của cậu không đến từ Cửu Vĩ, mà từ việc không bao giờ bỏ rơi bạn bè.',
		'payoff': 'Bài học: sức mạnh lớn nhất là tình bạn và ý chí.',
		'search_query': 'naruto anime fight scene'
	}],
	'cute_animals': [{
		'id': 'cute_new_01', 'topic': 'cute_animals',
		'hook': 'Mèo con lần đầu nhìn thấy tuyết',
		'body': 'Chú mèo con ba tháng tuổi lần đầu tiên trong đời nhìn thấy tuyết rơi. Nó vừa sợ vừa tò mò, cứ nhảy lên đuổi theo từng bông tuyết.',
		'payoff': 'Sự ngây thơ của mèo con khiến ai cũng phải mỉm cười.',
		'search_query': 'cute kitten snow first time'
	}],
	'meme': [{
		'id': 'meme_new_01', 'topic': 'meme',
		'hook': 'Khi mẹ gọi dậy đi học lúc 5 giờ sáng',
		'body': 'Cảnh tượng ai cũng từng trải qua: mẹ mở cửa phòng, bật đèn, và hét lên. Bạn thì chỉ muốn ngủ thêm năm phút.',
		'payoff': 'Nhưng năm phút đó kéo dài thành cả tiếng đồng hồ!',
		'search_query': 'funny morning meme'
	}]
}

NEW_VILEVI = {
	'whatif': [{
		'id': 'whatif_new_01', 'topic': 'whatif',
		'hook': 'Điều gì xảy ra nếu Mặt Trời đột ngột tắt?',
		'body': 'Trong 8 phút đầu, chúng ta vẫn thấy ánh sáng cũ. Sau đó, nhiệt độ Trái Đất sẽ giảm xuống âm 100 độ C trong vài tuần.',
		'payoff': 'Sự sống sẽ chỉ tồn tại quanh các miệng núi lửa và lỗ khoan sâu.',
		'search_query': 'sun going out simulation'
	}],
	'facts': [{
		'id': 'facts_new_01', 'topic': 'facts',
		'hook': 'Vì sao bầu trời có màu xanh?',
		'body': 'Ánh sáng Mặt Trời chứa mọi màu, nhưng phân tử không khí tán xạ ánh sáng xanh nhiều hơn các màu khác. Hiện tượng này gọi là tán xạ Rayleigh.',
		'payoff': 'Đó cũng là lý do hoàng hôn có màu đỏ cam.',
		'search_query': 'rayleigh scattering sky blue'
	}],
	'curiosity': [{
		'id': 'curio_new_01', 'topic': 'curiosity',
		'hook': 'Cá heo có thể nhận ra mình trong gương không?',
		'body': 'Cá heo là một trong số ít loài động vật vượt qua bài kiểm tra gương. Chúng biết đó là hình ảnh của chính mình, không phải con cá heo khác.',
		'payoff': 'Chỉ con người, cá heo, tinh tinh và voi mới làm được điều này.',
		'search_query': 'dolphin mirror self awareness'
	}],
	'food': [{
		'id': 'food_new_01', 'topic': 'food',
		'hook': 'Phở Việt Nam có nguồn gốc từ đâu?',
		'body': 'Phở ra đời đầu thế kỷ 20 tại Nam Định và Hà Nội. Nó kết hợp kỹ thuật nấu nước dùng của Pháp với nguyên liệu bản địa Việt Nam.',
		'payoff': 'Ngày nay phở là món Việt được biết đến nhiều nhất thế giới.',
		'search_query': 'vietnamese pho origin history'
	}]
}


def add_to(cid, new_data):
	p = os.path.join('channels', cid, 'content_db.json')
	d = json.load(io.open(p, encoding='utf-8'))
	added = 0
	for kind, items in new_data.items():
		if kind not in d:
			d[kind] = []
		existing = set(it.get('id') for it in d[kind])
		for it in items:
			if it['id'] not in existing:
				d[kind].insert(0, it)
				added += 1
	json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
	print(cid, 'added', added)


add_to('Mialinhcute', NEW_MIA)
add_to('vilevi5676', NEW_VILEVI)
