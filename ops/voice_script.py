# ops/voice_script.py - Chuan hoa text truoc khi TTS: co dau, ngat cau, tach CTA, pause cam xuc
import os, re
U = chr(95)
DOT = chr(46)
NL = chr(10)

# Map khong dau -> co dau cho cac tu tieng Viet pho bien
DIACRITIC_MAP = {
	'meo': 'mèo', 'cho': 'chó', 'con': 'con', 'ngu': 'ngủ', 'tren': 'trên', 'cua': 'cửa', 'so': 'sổ',
	'ngam': 'ngắm', 'mua': 'mưa', 'roi': 'rồi', 'that': 'thật', 'de': 'dễ', 'thuong': 'thương',
	'khi': 'khi', 'troi': 'trời', 'lam': 'làm', 'gi': 'gì', 'the': 'thế', 'nao': 'nào',
	'dang': 'đang', 'nhung': 'nhưng', 'cung': 'cũng', 'rat': 'rất', 'qua': 'quá', 'nhe': 'nhé',
	'minh': 'mình', 'ban': 'bạn', 'toi': 'tôi', 'chung': 'chúng', 'ta': 'ta', 'ho': 'họ',
	'vui': 'vui', 'buon': 'buồn', 'dep': 'đẹp', 'xinh': 'xinh', 'hay': 'hay', 'tuyet': 'tuyệt',
	'yeu': 'yêu', 'thich': 'thích', 'ghet': 'ghét', 'cuoi': 'cười', 'khoc': 'khóc',
	'theo': 'theo', 'doi': 'dõi', 'kenh': 'kênh', 'like': 'like', 'share': 'share', 'cmt': 'comment',
	'bai': 'bài', 'video': 'video', 'clip': 'clip', 'noi': 'nội', 'dung': 'dung', 'giup': 'giúp',
	'cau': 'câu', 'chuyen': 'chuyện', 'ke': 'kể', 'nghe': 'nghe', 'hieu': 'hiểu', 'biet': 'biết',
	'thay': 'thấy', 'nhin': 'nhìn', 'ngoi': 'ngồi', 'dung': 'đứng', 'chay': 'chạy', 'di': 'đi',
}

# Cac tu ket thuc cau -> pause dai
PAUSE_END_SENTENCE = 0.5
PAUSE_COMMA = 0.25
PAUSE_CTA_BEFORE = 0.7
PAUSE_CTA_AFTER = 0.3


def has_diacritics(text):
	if not text:
		return False
	for ch in text:
		code = ord(ch)
		if 0x00C0 <= code <= 0x024F or 0x1EA0 <= code <= 0x1EFF:
			return True
	return False


def add_diacritics_simple(text):
	# Rule-based don gian: map tung tu
	if not text:
		return text
	words = re.split(r'(\s+)', text)
	out = []
	for w in words:
		lw = w.lower().strip('.,!?:;"' + chr(39))
		if lw in DIACRITIC_MAP:
			fixed = DIACRITIC_MAP[lw]
			if w[:1].isupper():
				fixed = fixed[:1].upper() + fixed[1:]
			# Giu dau cau
			tail = w[len(lw):] if len(w) > len(lw) else ''
			out.append(fixed + tail)
		else:
			out.append(w)
	return ''.join(out)


def restore_diacritics(text, timeout=45):
	# Phuc hoi dau: goi free_llm json_mode=False -> text sach co dau; fallback map
	if not text or has_diacritics(text):
		return text
	try:
		from providers import free_llm as _fl
		pr = 'Them dau tieng Viet day du cho doan sau. Chi tra ve dung 1 dong van ban tieng Viet co dau, giu nguyen y nghia va do dai, KHONG giai thich, KHONG them y.'
		pr += NL + 'Doan goc: ' + text
		r = _fl.chat([{'role': 'user', 'content': pr}], max_tokens=220, json_mode=False)
		out = ((r or {}).get('text') or '').strip()
		out = out.split(NL)[0].strip()
		if out and has_diacritics(out):
			return out
	except Exception:
		pass
	return add_diacritics_simple(text)


def rewrite_via_ollama(text, timeout=60):
	# Goi Ollama de viet lai co dau + cam xuc
	try:
		from ops import ai_content as ac
		prompt = 'Viet lai doan sau bang tieng Viet CO DAU, tu nhien, co cam xuc, nhu nguoi ke chuyen. Giu y nghia, chia thanh 2-3 cau ngan. Tra ve chi text, khong giai thich.' + NL + NL + 'Doan goc: ' + text
		r = ac._call_ollama(prompt, temperature=0.6, max_tokens=200, timeout=timeout)
		r = (r or '').strip()
		if r and has_diacritics(r):
			return r
	except Exception:
		pass
	return None


def split_sentences(text):
	if not text:
		return []
	t = text.replace('!', '.').replace('?', '.')
	parts = [p.strip() for p in t.split('.') if p.strip()]
	return parts


def build_script(item, mode='full'):
	# mode='full' -> hook + body + payoff + CTA; 'no_cta' -> bo CTA
	hook = (item.get('hook') or '').strip()
	body = (item.get('body') or '').strip()
	payoff = (item.get('payoff') or '').strip()
	cta = (item.get('cta') or '').strip()

	# Chuan hoa co dau neu can
	all_text = ' '.join([hook, body, payoff])
	if not has_diacritics(all_text):
		# Thu ollama truoc
		fixed = rewrite_via_ollama(all_text)
		if fixed:
			hook = fixed
			body = ''
		else:
			hook = add_diacritics_simple(hook)
			body = add_diacritics_simple(body)
			payoff = add_diacritics_simple(payoff)

	if not has_diacritics(cta):
		cta = add_diacritics_simple(cta) if cta else ''

	# Ghep thanh cau
	sentences = []
	for part in [hook, body, payoff]:
		if part:
			sentences.extend(split_sentences(part))

	# Loc CTA ra rieng
	cta_final = cta
	if not cta_final:
		for s in list(sentences):
			low = s.lower()
			if any(k in low for k in ['theo doi', 'dang ky', 'subcribe', 'subscribe', 'like', 'share']):
				cta_final = s
				sentences.remove(s)
				break
	return {'sentences': sentences, 'cta': cta_final, 'full_text': ' '.join(sentences) + (' ' + cta_final if cta_final else '')}


if __name__ == '__main__':
	import json
	item = {'hook': 'Meo con dang lam gi khi troi mua?', 'body': 'Meo con ngu tren cua so ngam tung giot mua roi', 'payoff': 'That binh yen!', 'cta': 'Theo doi kenh nhe'}
	print(json.dumps(build_script(item), ensure_ascii=False, indent=2))
