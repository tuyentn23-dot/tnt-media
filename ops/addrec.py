p = 'pipeline/runner.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
Q = chr(39)
marker = 'def run_job(job, dry_run=False):'
insert = marker + NL + T + 'try:' + NL + T2 + 'from pipeline import recovery as _rec' + NL + T2 + '_rec.recover_stale_jobs()' + NL + T + 'except Exception:' + NL + T*2 + 'pass'
if marker not in src:
	print('marker not found')
	sys.exit(1)
src = src.replace(marker, insert, 1)
open(p, 'w', encoding='utf-8', newline='').write(src)
print('added recovery call')
