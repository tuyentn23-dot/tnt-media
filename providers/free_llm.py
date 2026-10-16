# -- coding: utf-8 --
# providers/free_llm.py
# Adapter doc lap cho cac LLM API mien phi (Groq, Gemini, OpenRouter).
# Khong sua core TNT AI - chi la adapter Media-specific theo policy.
import os, json
import requests

TIMEOUT = 60

FREE_PROVIDERS = {
	'groq': {
		'base': 'https://api.groq.com/openai/v1',
		'env': 'GROQ_API_KEY',
		'model': 'qwen/qwen3.8-27b',
		'kind': 'openai',
	},
	'gemini': {
		'base': 'https://generativelanguage.googleapis.com/v1beta/openai',
		'env': 'GEMINI_API_KEY',
		'model': 'gemini-2.5-flash',
		'kind': 'openai',
	},
	'openrouter': {
		'base': 'https://openrouter.ai/api/v1',
		'env': 'OPENROUTER_API_KEY',
		'model': 'meta-llama/llama-3.3-70b-instruct:free',
		'kind': 'openai',
	},
	'mistral': {
		'base': 'https://api.mistral.ai/v1',
		'env': 'MISTRAL_API_KEY',
		'model': 'mistral-small-latest',
		'kind': 'openai',
	},
}


def _key(name):
	return (os.environ.get(name) or '').strip()


def available():
	out = []
	for name, cfg in FREE_PROVIDERS.items():
		if _key(cfg['env']):
			out.append(name)
	return out


def _call_openai_style(base, key, model, messages, temperature=0.7, max_tokens=1024, extra_headers=None, json_mode=False):
	h = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}
	if extra_headers:
		h.update(extra_headers)
	body = {
		'model': model,
		'messages': messages,
		'temperature': temperature,
		'max_tokens': max_tokens,
	}
	if json_mode:
		body['response_format'] = {'type': 'json_object'}
	r = requests.post(base.rstrip('/') + '/chat/completions', headers=h, json=body, timeout=TIMEOUT)
	if r.status_code >= 400:
		raise RuntimeError(str(r.status_code) + ' ' + r.text[:300])
	d = r.json()
	return d['choices'][0]['message']['content']


def chat(messages, provider=None, **kw):
	order = [provider] if provider else available()
	last = None
	for name in order:
		if not name or name not in FREE_PROVIDERS:
			continue
		cfg = FREE_PROVIDERS[name]
		key = _key(cfg['env'])
		if not key:
			continue
		try:
			extra = {}
			if name == 'openrouter':
				extra = {'HTTP-Referer': 'https://tnt.local', 'X-Title': 'TNT Media Studio'}
			return {'ok': True, 'provider': name, 'text': _call_openai_style(cfg['base'], key, cfg['model'], messages, extra_headers=extra, **kw)}
		except Exception as e:
			last = name + ': ' + str(e)[:200]
	return {'ok': False, 'error': last or 'no free provider key set', 'tried': order}


def summarize_for_script(item):
	sys = 'Ban la bien tap video ngan Viet Nam. Tra ve JSON: hook, body, payoff, cta.'
	user = 'Chu de: ' + str((item or {}).get('topic') or (item or {}).get('hook') or '')
	res = chat([{'role': 'system', 'content': sys}, {'role': 'user', 'content': user}])
	if not res.get('ok'):
		return res
	txt = res.get('text') or ''
	try:
		s = txt[txt.find('{'):txt.rfind('}') + 1]
		data = json.loads(s)
		data['_provider'] = res.get('provider')
		return {'ok': True, 'data': data}
	except Exception:
		return {'ok': True, 'data': {'body': txt}, '_provider': res.get('provider')}


def vision_analyze(image_path_or_url, question='Mo ta noi dung chinh cua anh/video nay.'):
	prov = 'gemini' if _key('GEMINI_API_KEY') else None
	if not prov:
		return {'ok': False, 'error': 'GEMINI_API_KEY not set (vision requires Gemini)'}
	key = _key('GEMINI_API_KEY')
	msgs = [{'role': 'user', 'content': [
		{'type': 'text', 'text': question},
		{'type': 'image_url', 'image_url': {'url': image_path_or_url}},
	]}]
	try:
		text = _call_openai_style(FREE_PROVIDERS['gemini']['base'], key, FREE_PROVIDERS['gemini']['model'], msgs)
		return {'ok': True, 'provider': 'gemini', 'text': text}
	except Exception as e:
		return {'ok': False, 'error': str(e)[:300]}
