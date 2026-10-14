import sys, os, pickle, json
BASE = 'D:/TNT_AI/venture_foundry/media'
sys.path.insert(0, BASE)
os.chdir(BASE)
out = {}
tp = BASE + '/config/token.pickle'
if not os.path.exists(tp):
 tp = BASE + '/token.pickle'
f = open(tp, 'rb')
creds = pickle.load(f)
f.close()
out['scopes'] = list(getattr(creds, 'scopes', []) or [])
from googleapiclient.discovery import build
ya = build('youtubeAnalytics', 'v2', credentials=creds)
# Test basic query
q = ya.reports().query(ids='channel==MINE', startDate='2026-09-13', endDate='2026-10-10', metrics='views,estimatedMinutesWatched,subscribersGained,subscribersLost,averageViewDuration,averageViewPercentage', dimensions='day')
r = q.execute()
out['rows'] = len(r.get('rows', []))
out['sample'] = r.get('rows', [])[-3:]
# traffic sources
q2 = ya.reports().query(ids='channel==MINE', startDate='2026-09-13', endDate='2026-10-10', metrics='views', dimensions='insightTrafficSourceType')
r2 = q2.execute()
out['traffic'] = r2.get('rows', [])
# top videos
try:
 q3 = ya.reports().query(ids='channel==MINE', startDate='2026-09-13', endDate='2026-10-10', metrics='views,estimatedMinutesWatched,averageViewPercentage', dimensions='video', sort='-views', maxResults=10)
 r3 = q3.execute()
 out['top_by_analytics'] = r3.get('rows', [])
except Exception as e:
 out['top_err'] = str(e)[:200]
open(BASE + '/_ya_out.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=2, default=str))
print('DONE')
