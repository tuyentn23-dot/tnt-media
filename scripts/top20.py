import json, re
rows = json.load(open('analytics/all_videos.json', encoding='utf-8'))
top = sorted(rows, key=lambda r: r['views'], reverse=True)[:20]
print('=== TOP 20 VIDEO ===')
for r in top:
	t = r['title'].encode('ascii', 'replace').decode()
	print(r['views'], '|', r['dur'], '|', t[:55])
