import json, re
rows = json.load(open('analytics/all_videos.json', encoding='utf-8'))
# loc video that (views>100)
hot = [r for r in rows if r['views'] > 1000]
print('HOT (>1k views):', len(hot), '/', len(rows))
# thong ke theo so giay
def secs(d):
	m = re.match(r'PT(?:([0-9]+)M)?(?:([0-9]+)S)?', d)
	if not m:
		return 0
	return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)
for r in rows:
	r['sec'] = secs(r['dur'])
# views trung binh theo nhom thoi luong
import statistics as stx
short10 = [r['views'] for r in rows if r['sec'] <= 12]
mid = [r['views'] for r in rows if 13 <= r['sec'] <= 20]
longv = [r['views'] for r in rows if r['sec'] > 20]
print('<=12s:', len(short10), 'avg', int(stx.mean(short10)) if short10 else 0)
print('13-20s:', len(mid), 'avg', int(stx.mean(mid)) if mid else 0)
print('>20s:', len(longv), 'avg', int(stx.mean(longv)) if longv else 0)
