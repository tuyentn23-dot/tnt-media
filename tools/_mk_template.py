import io, os, json
NL = chr(10)
Q = chr(34)
d = os.path.join('channels', '_template')
os.makedirs(d, exist_ok=True)
cfg = {
	'id': 'template',
	'name': 'Template Channel',
	'enabled': False,
	'token_file': 'config/token.pickle',
	'style': {
		'language': 'vi',
		'voice': 'female_soft',
		'music_genre': 'mystery',
		'color_primary': '#1a1a2e',
		'color_accent': '#e94560',
		'font': 'Arial-Bold',
		'font_size': 70,
		'watermark': '@template',
		'intro_seconds': 0.8,
		'outro_seconds': 1.2,
		'aspect': '9:16',
		'max_duration_sec': 58,
	},
	'content': {
		'kinds': ['whatif'],
		'category_id': '28',
		'tags_base': ['shorts'],
		'title_template': '{hook}',
		'desc_template': '{body} {payoff}',
		'topic_pool_file': 'topic_pool.json',
	},
	'schedule': {
		'enabled': False,
		'interval_min': 60,
		'batch': 2,
		'post_hours': [6, 11, 15, 19, 22],
	},
}
io.open(os.path.join(d, 'channel.json'), 'w', encoding='utf-8').write(json.dumps(cfg, ensure_ascii=False, indent=2))
content = {'whatif': [{'id': 'sample_1', 'topic': 'example', 'hook': 'Vi du hook.', 'body': 'Noi dung.', 'payoff': 'Ket luan.', 'question': 'Ban nghi sao?'}]}
io.open(os.path.join(d, 'content_db.json'), 'w', encoding='utf-8').write(json.dumps(content, ensure_ascii=False, indent=2))
pool = {'whatif': ['neu mat troi bien mat', 'neu ban khong bao gio ngu'], 'facts': ['su that ve nao bo']}
io.open(os.path.join(d, 'topic_pool.json'), 'w', encoding='utf-8').write(json.dumps(pool, ensure_ascii=False, indent=2))
print('TEMPLATE RECREATED')
