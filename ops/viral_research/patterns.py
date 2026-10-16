# -- coding: utf-8 --
# ops/viral_research/patterns.py
# Phan tich pattern tu metadata video viral (khong tai video).
import re, json, statistics


HOOK_WORDS = [
	'bi mat', 'su that', 'khong the tin', 'bat ngo', 'gay soc', 'to mo',
	'ban co biet', 'tai sao', 'the nao', 'bao nhieu', 'co the', 'hau qua',
	'nguy hiem', 'than ky', 'kinh khung', 'cuc', 'sieu', 'nhat', 'top',
]

EMOJI_RE = re.compile('[' + chr(0x1F300) + '-' + chr(0x1FAFF) + chr(0x2600) + '-' + chr(0x27BF) + ']')
NUMBER_RE = re.compile(r'(\d+)')


def analyze_title(t):
	t = str(t or '').strip()
	low = t.lower()
	hook_hits = [w for w in HOOK_WORDS if w in low]
	return {
		'len': len(t),
		'has_number': bool(NUMBER_RE.search(t)),
		'has_question': '?' in t,
		'has_exclaim': '!' in t,
		'has_emoji': bool(EMOJI_RE.search(t)),
		'hook_words': hook_hits,
		'hook_score': len(hook_hits),
		'starts_upper': t[:1].isupper() if t else False,
	}


def analyze_item(it):
	a = analyze_title(it.get('title'))
	d = int(it.get('duration_s') or 0)
	v = int(it.get('views') or 0)
	l = int(it.get('likes') or 0)
	return {
		'id': it.get('id'),
		'title': it.get('title'),
		'channel': it.get('channel'),
		'platform': it.get('platform'),
		'views': v,
		'likes': l,
		'duration_s': d,
		'engagement_rate': round(l / v, 4) if v else 0,
		'title_pattern': a,
	}


def summarize(items):
	if not items:
		return {'count': 0}
	parsed = [analyze_item(it) for it in items]
	views = [p['views'] for p in parsed if p['views']]
	durs = [p['duration_s'] for p in parsed if p['duration_s']]
	eng = [p['engagement_rate'] for p in parsed if p['engagement_rate']]
	scores = [p['title_pattern']['hook_score'] for p in parsed]
	qs = sum(1 for p in parsed if p['title_pattern']['has_question'])
	ns = sum(1 for p in parsed if p['title_pattern']['has_number'])
	es = sum(1 for p in parsed if p['title_pattern']['has_emoji'])
	return {
		'count': len(parsed),
		'views_median': int(statistics.median(views)) if views else 0,
		'views_max': max(views) if views else 0,
		'duration_median_s': int(statistics.median(durs)) if durs else 0,
		'engagement_median': round(statistics.median(eng), 4) if eng else 0,
		'hook_score_avg': round(sum(scores) / len(scores), 2) if scores else 0,
		'pct_question_title': round(100.0 * qs / len(parsed), 1),
		'pct_number_title': round(100.0 * ns / len(parsed), 1),
		'pct_emoji_title': round(100.0 * es / len(parsed), 1),
		'top5': sorted(parsed, key=lambda x: -x['views'])[:5],
	}


def suggest_recipe(items, kind='facts'):
	s = summarize(items)
	return {
		'kind': kind,
		'summary': s,
		'recipe': {
			'title_len_target': min(80, max(30, s.get('hook_score_avg', 0) * 10 + 40)),
			'use_question': s.get('pct_question_title', 0) > 30,
			'use_number': s.get('pct_number_title', 0) > 30,
			'use_emoji': s.get('pct_emoji_title', 0) > 30,
			'duration_target_s': s.get('duration_median_s', 30) or 30,
		},
	}
