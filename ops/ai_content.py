# ai_content.py - generate viral facts via OpenAI (tab-indent)
import os, json, requests
ROOT = os.getcwd()

def _key():
	env = os.path.join(ROOT, '.env')
	txt = open(env, encoding='utf-8').read() if os.path.exists(env) else ''
	return next((l.split('=', 1)[1].strip() for l in txt.splitlines() if l.startswith('OPENAI_API_KEY')), '')

PROMPT = ""
TOPICS = ['space', 'ocean', 'animal', 'body', 'brain', 'food', 'psychology', 'nature']

SYS = ('Ban la chuyen gia noi dung viral cho YouTube Shorts tieng Viet. '
	+ 'Tra ve DUY NHAT mot JSON array, moi phan tu la object voi cac key: '
	+ 'id, topic, hook, body, payoff, question, search_query. '
	+ 'hook la cau gay to mo manh (toi da 60 ky tu). body la 1-2 cau su that. '
	+ 'payoff la cau ket bat ngo. question la cau hoi tuong tac. '
	+ 'search_query la tieng Anh de tim footage. Khong giai thich gi them.')

def generate(topic, n=5, model='gpt-4o-mini'):
	key = _key()
	user = 'Tao ' + str(n) + ' su that thu vi ve chu de: ' + topic
	msgs = [{'role': 'system', 'content': SYS}, {'role': 'user', 'content': user}]
	body = {'model': model, 'messages': msgs, 'temperature': 0.9}
	hdr = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}
	r = requests.post('https://api.openai.com/v1/chat/completions', headers=hdr, json=body, timeout=60)
	data = r.json()
	ch = (data.get('choices') or [{}])[0]
	msg = ch.get('message', {})
	txt = (msg.get('content') or '[]').strip()
	return json.loads(txt)
