# pipeline/dash_stats.py - Thong ke cho Dashboard
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)
from pipeline import state


def views_by_day(days=7):
	'''Tra ve [{date, views, likes, count}] cho N ngay gan nhat.'''
	c = state.connect()
	import datetime
	today = datetime.date.today()
	out = []
	for i in range(days-1, -1, -1):
		d = today - datetime.timedelta(days=i)
		key = d.strftime('%Y-%m-%d')
		try:
			r = c.execute('SELECT COALESCE(SUM(view_count),0), COALESCE(SUM(like_count),0), COUNT() FROM publications WHERE substr(COALESCE(published_at, created_at),1,10)=?', (key,)).fetchone()
			v, lk, n = (r[0] or 0), (r[1] or 0), (r[2] or 0)
		except Exception:
			v, lk, n = 0, 0, 0
		out.append({'date': key, 'views': int(v), 'likes': int(lk), 'count': int(n)})
	c.close()
	return out


def summary():
	'''Tong hop KPI: pubs, views, likes, published, rendered.'''
	c = state.connect()
	out = {}
	try:
		r = c.execute('SELECT COUNT(), COALESCE(SUM(view_count),0), COALESCE(SUM(like_count),0) FROM publications').fetchone()
		out['pubs'] = int(r[0] or 0)
		out['views'] = int(r[1] or 0)
		out['likes'] = int(r[2] or 0)
	except Exception as e:
		out['err'] = str(e)[:80]
	for st in ('published', 'rendered', 'scheduled'):
		try:
			r = c.execute('SELECT COUNT() FROM publications WHERE status=?', (st,)).fetchone()
			out[st] = int(r[0] or 0)
		except Exception:
			out[st] = 0
	c.close()
	return out
