# -- coding: utf-8 --
import os, json

def _key():
	k = os.environ.get('OPENAI_API_KEY')
	if k:
		return k
	try:
		for line in open('.env', encoding='utf-8'):
			if line.startswith('OPENAI_API_KEY='):
				return line.split('=', 1)[1].strip()
	except Exception:
		pass
	return ''

def gen_script(topic, niche, lang='vi'):
	from openai import OpenAI
	client = OpenAI(api_key=_key())
	sys_p = 'Ban la chuyen gia viet kich ban YouTube Shorts tieng Viet. Tra ve JSON thuan.'
	parts = []
	parts.append('Chu de: ' + topic)
	parts.append('Niche: ' + niche)
	parts.append('Viet kich ban 30 giay, TIENG VIET CO DAU day du.')
	parts.append('Tra ve JSON voi cac truong: hook (cau gay to mo 3s), body (mang 3-4 cau ngan), payoff (cau ket bat ngo), cta (keu goi follow), title (<=60 ky tu), tags (mang 5 tag).')
	parts.append('Chi tra JSON thuan, khong giai thich.')
	user_p = chr(10).join(parts)
	r = client.chat.completions.create(
		model='gpt-4o-mini',
		messages=[
			{'role': 'system', 'content': sys_p},
			{'role': 'user', 'content': user_p},
		],
		temperature=0.8,
		response_format={'type': 'json_object'},
	)
	txt = r.choices[0].message.content
	try:
		return json.loads(txt)
	except Exception:
		return None
