import json
d = json.load(open('analytics/channel_videos.json', encoding='utf-8'))
print('=== LOW VIEW (<=50) ===')
for r in d:
    if r['views'] <= 50:
        t = r['Title'] if 'Title' in r else r['title']
        t = t.encode('ascii','replace').decode()
        print(r['views'], '|', r['published'][:10], '|', r['duration'], '|', t[:70])
print('=== RECENT 15 BY DATE ===')
for r in sorted(d, key=lambda x: x['published'], reverse=True)[:15]:
    t = r['title'].encode('ascii','replace').decode()
    print(r['views'], '|', r['published'][:10], '|', r['duration'], '|', t[:70])
