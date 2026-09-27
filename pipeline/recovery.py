# -- coding: utf-8 --
# pipeline/recovery.py - Khoi phuc job ket running
import time, datetime
from pipeline import state


def recover_stale_jobs(max_age_sec=900):
	c = state.init()
	try:
		rows = c.execute("SELECT id, updated_at FROM jobs WHERE status='running'").fetchall()
	except Exception:
		return 0
	now = time.time()
	n = 0
	for r in rows:
		try:
			t0 = datetime.datetime.strptime(r['updated_at'], '%Y-%m-%dT%H:%M:%S').timestamp()
			if now - t0 > max_age_sec:
				c.execute('UPDATE jobs SET status=?, error=? WHERE id=?', ('failed', 'stale running (recovery)', r['id']))
				n += 1
		except Exception:
			pass
	c.commit()
	return n


if __file__ == '__main__':
	print('recovered', recover_stale_jobs())
