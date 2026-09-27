p = 'pipeline/runner.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
marker = 'def run_job(job, dry_run=False):'
recovery = (
	'def recover_stale_jobs(max_age_sec=900):' + NL
	+ T + 'import time as _t' + NL
	+ T + 'from pipeline import state as _s' + NL
	+ T + 'c = _s.init()' + NL
	+ T + 'try:' + NL
	+ T2 + 'rows = c.execute(' + chr(39) + 'SELECT id, updated_at FROM jobs WHERE status=' + chr(39) + chr(39) + 'running' + chr(39) + chr(39) + chr(39) + ').fetchall()' + NL
	+ T + 'except Exception:' + NL
	+ T2 + 'return 0' + NL
	+ T + 'now = _t.time()' + NL
	+ T + 'n = 0' + NL
	+ T + 'for r in rows:' + NL
	+ T2 + 'try:' + NL
	+ T3 + 'import datetime as _dt' + NL
	+ T3 + 't0 = _dt.datetime.strptime(r[' + chr(39) + 'updated_at' + chr(39) + '], ' + chr(39) + '%Y-%m-%dT%H:%M:%S' + chr(39) + ').timestamp()' + NL
	+ T3 + 'if now - t0 > max_age_sec:' + NL
	+ T4 + 'c.execute(' + chr(39) + 'UPDATE jobs SET status=?, error=? WHERE id=?' + chr(39) + ', (' + chr(39) + 'failed' + chr(39) + ', ' + chr(39) + 'stale running' + chr(39) + ', r[' + chr(39) + 'id' + chr(39) + ']))' + NL
	+ T4 + 'n += 1' + NL
	+ T2 + 'except Exception:' + NL
	+ T3 + 'pass' + NL
	+ T + 'c.commit()' + NL
	+ T + 'return n' + NL + NL + NL
)
out = src.replace(marker, recovery + marker, 1)
open(p, 'w', encoding='utf-8', newline='').write(out)
print('added recovery')
