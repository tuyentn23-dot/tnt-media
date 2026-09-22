# channel_render.py - render theo style kenh, CHI giong VIET (tab)
import os, sys, json
sys.path.insert(0, os.getcwd())
from ops import ffmpeg_render as FR
ROOT = os.getcwd()

# CHI dung 2 giong Viet: female_north (HoaiMy), male_north (NamMinh)
STYLE_MAP = {
	'female_cute': ('female_north', 'cute'),
	'female_warm': ('female_north', 'story'),
	'female_soft': ('female_north', 'calm'),
	'female_north': ('female_north', 'hype'),
	'male_north': ('male_north', 'story'),
}

TOPIC_VOICE = {
	'space': ('male_north', 'story'),
	'psychology': ('female_north', 'calm'),
	'brain': ('male_north', 'story'),
	'whatif': ('male_north', 'story'),
}

def load_style(channel_id):
	p = os.path.join(ROOT, 'channels', channel_id, 'channel.json')
	cfg = json.load(open(p, encoding='utf-8'))
	return cfg.get('style', {})

def render_for(channel_id, item, out, scenes=6):
	st = load_style(channel_id)
	topic = (item.get('topic') or '').lower() or ((item.get('id') or '').split(chr(95))[0].lower())
	voice_key = st.get('voice', 'female_north')
	voice, preset = TOPIC_VOICE.get(topic) or STYLE_MAP.get(voice_key, ('female_north', 'hype'))
	accent = st.get('color_accent', '#e94560')
	hook_c = accent.replace('#', '0x')
	FR.set_style(cap='white', hook=hook_c, bar=hook_c)
	if topic == 'gacha':
		return FR.render_gacha(dict(item), out, voice=voice, preset=preset)
	return FR.render(dict(item), out, voice=voice, preset=preset, scenes=scenes)
