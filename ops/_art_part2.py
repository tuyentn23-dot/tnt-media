

def ollama(prompt, model=None, timeout=1800):
	import urllib.request
	model = model or os.environ.get('TNT_OLLAMA_MODEL', 'qwen2.5:7b')
	url = 'http://127.0.0.1:11434/api/generate'
	payload = json.dumps({'model': model, 'prompt': prompt, 'stream': False,
		'options': {'temperature': 0.8, 'num_predict': 4096}}).encode('utf-8')
	req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
	r = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8'))
	return (r.get('response') or '').strip()


def write_script(art, facts, sections=8):
	NL = chr(10)
	Q = chr(34)
	base = ('Ban la bien tap vien kenh documentary nghe thuat tieng Viet. '
		+ 'Viet kich ban video DAI 20 phut ve tac pham: ' + art + '.' + NL
		+ 'Thong tin nen: ' + facts + NL
		+ 'Yeu cau: giong ke bi an, ly ky, hap dan, chinh xac lich su, '
		+ 'khong bia dat vo can cu. Chia thanh ' + str(sections) + ' phan, moi phan 250-350 tu.' + NL
		+ 'Tra ve DUY NHAT mot doi tuong JSON voi cac khoa: title, hook, parts.'
		+ ' parts la mang cac doi tuong co heading va text.')
	txt = ollama(base)
	return _parse_json(txt)


def _parse_json(txt):
	if not txt:
		return None
	s = txt.strip()
	i = s.find('{')
	j = s.rfind('}')
	if i >= 0 and j > i:
		s = s[i:j+1]
	try:
		return json.loads(s)
	except Exception:
		return None
