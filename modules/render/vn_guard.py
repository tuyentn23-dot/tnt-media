# tool: vietnamese-guard
# -- coding: utf-8 --
# modules/render/vn_guard.py v1.0.0
# BAT BUOC: moi text tieng Viet phai co dau day du
import re
MODULE = {
	'tool': 'vietnamese-guard','name': 'render.vn_guard', 'version': '1.0.0', 'interface': 'check(text) -> dict', 'deps': []}
NO_DIA = set(['khong', 'duoc', 'nguoi', 'nhung', 'cung', 'voi', 'trong', 'nay', 'hay', 'nho', 'yeu', 'thuong', 'cuoc', 'song', 'ban', 'than', 'minh', 'dieu', 'lon', 'lao', 'dung', 'bao', 'gio', 'danh', 'gia', 'thap', 'meo', 'lam', 'nen', 'chu', 'cho', 'vui', 'nha', 'hoc', 'hoi', 'moi', 'ngay', 'tro', 'thanh', 'phien', 'tot', 'nhat', 'su', 'tu', 'chay', 'giay', 'toc', 'quan', 'bang', 'ben', 'gau', 'truc', 'tieng', 'an', 'tre'])
DIA_LOWER = 'ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ'
DIA = set(DIA_LOWER) | set(DIA_LOWER.upper())


def count_dia(text):
	if not text:
		return 0
	return sum(1 for c in text if c in DIA)


def count_bad(text):
	if not text:
		return 0
	low = str(text).lower()
	words = re.findall('[a-z]+', low)
	return sum(1 for w in words if w in NO_DIA)


def check(text):
	if not text or not str(text).strip():
		return {'ok': False, 'reason': 'empty'}
	s = str(text)
	d = count_dia(s)
	bad = count_bad(s)
	letters = sum(1 for c in s if c.isalpha())
	if letters < 15:
		return {'ok': True, 'diacritics': d, 'note': 'short'}
	# Khong co dau nao + text dai -> reject
	if d == 0:
		return {'ok': False, 'reason': 'no diacritics', 'diacritics': 0}
	# Co dau nhung > 70% tu suspect -> reject
	words = len(re.findall(chr(91) + chr(97) + chr(45) + chr(122) + chr(93) + chr(43), s.lower()))
	if words > 5 and bad > words * 0.7:
		return {'ok': False, 'reason': 'mostly no-diacritic', 'diacritics': d, 'suspect': bad, 'words': words}
	return {'ok': True, 'diacritics': d, 'suspect': bad, 'words': words}
def assert_vn(*texts):
	for t in texts:
		r = check(t)
		if not r['ok']:
			raise ValueError('VI pham tieng Viet co dau: ' + str(t)[:80])
	return True