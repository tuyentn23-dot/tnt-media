# -- coding: utf-8 --
# Script templates offline - tieng Viet co dau, khong can API
import os, json, random

_TPL = None

def _load():
	global _TPL
	if _TPL is not None:
		return _TPL
	_TPL = {}
	for p in ['config/scripts_vi.json', 'config/scripts_vi_extra.json']:
		if os.path.exists(p):
			try:
				d = json.load(open(p, encoding='utf-8'))
				if isinstance(d, dict):
					_TPL.update(d)
			except Exception:
				pass
	return _TPL

# Extra templates cho cac topic chua co trong scripts_vi.json
EXTRA = {
	'anime': {
		'hook': 'Meo cute gap anime',
		'lines': [
			'Nhung chu meo con cung co bo phim hoat hinh yeu thich.',
			'Chung thuong ngoi im lang nhu dang suy nghi ve nhan vat.',
			'Co chu con bat chay theo nhan vat tren man hinh.',
			'Hoa ra chung cung co the gioi tinh than phong phu.',
		],
		'cta': 'Theo doi Mia Linh de xem them nhe!',
	},
	'roblox': {
		'hook': 'Roblox - the gioi mini game',
		'lines': [
			'Roblox co hang trieu mini game mien phi cho moi nguoi.',
			'Ban co the tao nhan vat va the gioi cua rieng minh.',
			'Co the choi cung ban be o bat cu dau tren the gioi.',
			'Day la noi de thoa suc sang tao khong gioi han.',
		],
		'cta': 'Theo doi de kham pha them!',
	},
	'cute_animals': {
		'hook': 'Khoanh khac dong vat cute',
		'lines': [
			'Nhung chu cho con dang ngu trong long ban tay.',
			'Meo con choi dua voi cuon len.',
			'Tho con nhay tung tang trong vuon hoa.',
			'Moi khoanh khac deu khien trai tim am ap.',
		],
		'cta': 'Theo doi Mia Linh nhe!',
	},
	'gacha': {
		'hook': 'Gacha - tao nhan vat dinh cao',
		'lines': [
			'Gacha cho phep ban tao nhan vat voi hang nghin phu kien.',
			'Ban co the thiet ke trang phuc, kieu toc, bieu cam.',
			'Cong dong Gacha chia se hang trieu nhan vat moi ngay.',
			'Day la noi de thoa suc sang tao cua ban tre.',
		],
		'cta': 'Theo doi de xem them nhe!',
	},
	'lifestyle': {
		'hook': 'Bi quyet song vui moi ngay',
		'lines': [
			'Bat dau ngay moi bang mot nu cuoi va ly ca phe.',
			'Danh ba muoi phut doc sach thay vi luot dien thoai.',
			'Di bo hai muoi phut giup tinh than minh man.',
			'Cuoc song tuoi dep khi ta biet chan chu tung phut.',
		],
		'cta': 'Theo doi ViLe Vi de song vui hon!',
	},
	'food': {
		'hook': 'Am thuc Viet - huong vi dam da',
		'lines': [
			'Pho Ha Noi dam da huong quế hoi.',
			'Banh mi Sai Gon gion ruoi voi nhan phong phu.',
			'Com tam mien Nam thom mui dua nuong.',
			'Moi mon an deu mang mot cau chuyen rieng.',
		],
		'cta': 'Theo doi de kham pha them!',
	},
	'nostalgia': {
		'hook': 'Ky uc tuoi tho - nhung nam thang dep',
		'lines': [
			'Nhung buoi chieu he choi o quan voi ban be.',
			'Tieng ve keu trong nhung buoi trua he.',
			'Man choi dien tu va nhung tro choi dan gian.',
			'Ky uc tuoi tho la vien ngoc quy trong tim.',
		],
		'cta': 'Theo doi de song lai ky uc!',
	},
	'facts': {
		'hook': 'Su that khoa hoc ban chua biet',
		'lines': [
			'Co nhung su that khien ban phai giat minh.',
			'Khoa hoc da chung minh nhieu dieu thu vi.',
			'The gioi xung quanh chua day dieu ky dieu.',
			'Hoc moi ngay de hieu biet them.',
		],
		'cta': 'Theo doi de hoc them!',
	},
	'curiosity': {
		'hook': 'Su that thu vi ban chua tung biet',
		'lines': [
			'Co nhung su that khien ban bat ngo.',
			'The gioi nay day dieu ky la.',
			'Moi ngay ta co the hoc dieu moi.',
			'Hay giu long to mo de kham pha.',
		],
		'cta': 'Theo doi de kham pha!',
	},
	'psychology': {
		'hook': 'Tam ly hoc - hieu minh de song tot',
		'lines': [
			'Não bo chung ta luon tim kiem su an toan.',
			'Cam xuc khong phai la yeu duoi ma la suc manh.',
			'Hieu minh la buoc dau de thay doi.',
			'Moi nguoi deu co the phat trien ban than.',
		],
		'cta': 'Theo doi de hieu minh hon!',
	},
	'whatif': {
		'hook': 'Neu the gioi thay doi - dieu gi xay ra?',
		'lines': [
			'Neu trai dat ngung quay, moi thu se dao lon.',
			'Neu mat troi tat, trai dat lanh gia trong vai ngay.',
			'Neu con nguoi song duoi nuoc, cuoc song se khac.',
			'Nhung kich ban nay giup ta hieu gia tri hien tai.',
		],
		'cta': 'Theo doi de kham pha them!',
	},
	'science': {
		'hook': 'Khoa hoc - chan troi tri thuc',
		'lines': [
			'Khoa hoc giup chung ta hieu ve the gioi.',
			'Tu y hoc den vu tru, moi linh vuc deu thu vi.',
			'Nhung phat minh moi thay doi cuoc song.',
			'Hoc khoa hoc la hoc cach tu duy.',
		],
		'cta': 'Theo doi de hoc khoa hoc!',
	},
	'nature': {
		'hook': 'Thien nhien - nguon cam hung',
		'lines': [
			'Rung xanh bat tan mang lai binh yen.',
			'Suoi trong lanh giup tam hon thu gian.',
			'Bai bien cat vang goi bao ky nghi.',
			'Thien nhien la mon qua vo gia.',
		],
		'cta': 'Theo doi de thu gian!',
	},
}

def get(topic):
	"""Tra ve template cho topic. Fallback qua EXTRA neu khong co trong JSON."""
	d = _load()
	if topic in d:
		v = d[topic]
		if isinstance(v, dict) and 'hook' in v and 'lines' in v:
			return v
	if topic in EXTRA:
		return EXTRA[topic]
	# fallback generic
	return {
		'hook': 'Kham pha ' + topic,
		'lines': [
			'Hom nay chung ta cung tim hieu ve ' + topic + '.',
			'Co nhieu dieu thu vi ban chua biet.',
			'Moi chi tiet deu dang kham pha.',
			'Hay cung xem het video nhe.',
		],
		'cta': 'Theo doi de xem them!',
	}

def to_segments(topic, voice_speed=1.0):
	"""Tra ve (voice_text, hook, captions) cho topic."""
	t = get(topic)
	hook = t['hook']
	lines = list(t['lines'])
	cta = t.get('cta', 'Theo doi de xem them!')
	voice = hook + '. ' + ' '.join(lines) + ' ' + cta
	captions = [hook] + lines + [cta]
	return voice, hook, captions
