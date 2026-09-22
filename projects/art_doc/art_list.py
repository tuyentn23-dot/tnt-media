# -- coding: utf-8 --
"""10 famous paintings for art-documentary videos.

Each entry: slug, Vietnamese display title, Wikimedia Commons file name,
background facts (Vietnamese, for the LLM script writer).
"""

ARTS = [
	{
		'slug': 'mona_lisa',
		'title': 'Mona Lisa',
		'file': 'Mona_Lisa,_by_Leonardo_da_Vinci,from_C2RMF_retouched.jpg',
		'facts': ('Mona Lisa cua Leonardo da Vinci, ve khoang 1503-1519, hien o bao tang Louvre Paris. '
			'Nu cuoi bi an, anh mat nhu doi theo nguoi xem. Bi danh La Gioconda. '
			'1911 bi danh cap boi Vincenzo Peruggia, mat 2 nam moi tim lai. Tranh nho 77x53cm tren go duong.'),
	},
	{
		'slug': 'starry_night',
		'title': 'The Starry Night',
		'file': 'Van_Gogh-Starry_Night-_Google_Art_Project.jpg',
		'facts': ('The Starry Night cua Vincent van Gogh, ve 1889 khi o tu vien Saint-Remy. '
			'Ve tu tri nho khung cua so phong benh. Bui troi xoay cuon, 11 ngoi sao, mat trang loi. '
			'Van Gogh ve khi tinh than bat on, ban than thay buc tranh that bai.'),
	},
	{
		'slug': 'the_scream',
		'title': 'The Scream',
		'file': 'Edvard_Munch,_1893,_The_Scream,_oil,_tempera_and_pastel_on_cardboard,_91_x_73_cm,National_Gallery_of_Norway.jpg',
		'facts': ('The Scream cua Edvard Munch, 1893, bieu tuong cua noi lo au hien dai. '
			'Munch ke cam hung khi thay bau troi do nhu mau, nghe tieng thet vo tan. '
			'Co 4 phien ban. Nam 1994 va 2004 bi danh cap roi tim lai. Bieu tuong cua chung khoan lo au.'),
	},
	{
		'slug': 'girl_pearl_earring',
		'title': 'Girl with a Pearl Earring',
		'file': 'Meisje_met_de_parel.jpg',
		'facts': ('Girl with a Pearl Earring cua Johannes Vermeer, khoang 1665. '
			'Duoc goi la Mona Lisa cua phuong Bac. Co gai vo danh, khong phai chan dung that. '
			'Ngoc trai thuc ra co the chi la thuy tinh. Anh sang va bo cuc bac thay Vermeer.'),
	},
	{
		'slug': 'last_supper',
		'title': 'The Last Supper',
		'file': 'The_Last_Supper-Leonardo_Da_Vinci-High_Resolution_32x16.jpg',
		'facts': ('The Last Supper cua Leonardo da Vinci, 1495-1498, tuong bich o Milan. '
			'Ve bua an cuoi cua Chu Gia. Da Vinci thu nghiem chat lieu kho, tranh bong troc som. '
			'Trong chiến tranh Napoleon, binh linh dung lam bia ban. Phuc chec hang tram nam.'),
	},
	{
		'slug': 'guernica',
		'title': 'Guernica',
		'file': 'Picasso-Guernica-Google_Art_Project.jpg',
		'facts': ('Guernica cua Pablo Picasso, 1937, phan doi chien tranh. '
			'Lay cam hung tu vu bom thi tran Guernica trong noi chien Tay Ban Nha. '
			'Buc tranh den trang xam, khong mau. Picasso cam khong cho nazi xem.'),
	},
	{
		'slug': 'persistence_memory',
		'title': 'The Persistence of Memory',
		'file': 'The_Persistence_of_Memory.jpg',
		'facts': ('The Persistence of Memory cua Salvador Dali, 1931, bieu tuong sieu thuc. '
			'Dong ho mem chay nhu tan chay tren canh cay va khuon mat. '
			'Dali noi lay cam hung tu pho mat chay. Ten buc tranh lien quan thoi gian troi.'),
	},
	{
		'slug': 'american_gothic',
		'title': 'American Gothic',
		'file': 'Grant_Wood-American_Gothic-Google_Art_Project.jpg',
		'facts': ('American Gothic cua Grant Wood, 1930. Nguoi dan ong cam chia ba, nguoi phu nu. '
			'Hinh mau dua theo anh chi cua hoa si va nha tho. Bieu tuong nong thon My. '
			'Bi hieu nham la chan dung vo chong trong khi la cha va con gai.'),
	},
	{
		'slug': 'birth_of_venus',
		'title': 'The Birth of Venus',
		'file': 'Sandro_Botticelli-La_nascita_di_Venere-Google_Art_Project-_edited.jpg',
		'facts': ('The Birth of Venus cua Sandro Botticelli, khoang 1485, y thanh Venus noi len tu vo so. '
			'Buc tranh than thoai, mot trong nhung tac pham dau tien ve co the nu khoa than. '
			'Tung bi coi la dung ngai, che khuat nhieu nam. Nay la bieu tuong thoi Phuc Hung.'),
	},
	{
		'slug': 'nighthawks',
		'title': 'Nighthawks',
		'file': 'Nighthawks_by_Edward_Hopper_1942.jpg',
		'facts': ('Nighthawks cua Edward Hopper, 1942. Quan an dem khuya, anh sang vang, 4 nguoi xa la. '
			'Lay cam hung tu mot quan an o New York. Bieu tuong noi co don do thi My. '
			'Khong co cua ra vao ro rang, giam cam giac bi nhot. Lien quan tranh chien tranh.'),
	},
]
