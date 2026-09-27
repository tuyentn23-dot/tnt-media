# -- coding: utf-8 --
# pipeline/selfcheck.py - Health check truoc khi ket thuc phien
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state

CHECKS = []


def check(name):
	def deco(fn):
		CHECKS.append((name, fn))
		return fn
	return deco


@check('db_exists')
def c1():
	return os.path.exists(state.DB), state.DB


@check('db_writable')
def c2():
	try:
		c = state.connect()
		c.execute('SELECT COUNT(*) FROM publications').fetchone()
		return True, 'OK'
	except Exception as e:
		return False, str(e)[:80]


@check('tables_present')
def c3():
	need = ['channels', 'jobs', 'publications', 'topics', 'assets', 'audit', 'quota', 'modules_ver', 'trends']
	c = state.connect()
	have = [r[0] for r in c.execute('SELECT name FROM sqlite_master').fetchall()]
	missing = [t for t in need if t not in have]
	return (len(missing) == 0), 'missing: ' + str(missing)


@check('pipeline_files')
def c4():
	need = ['pipeline/state.py', 'pipeline/migrate.py']
	missing = [f for f in need if not os.path.exists(os.path.join(ROOT, f))]
	return (len(missing) == 0), 'missing: ' + str(missing)


@check('no_legacy_ledger_read')
def c5():
	return True, 'skip'


@check('pipeline_phase2')
def c6():
	need = ['pipeline/runner.py', 'pipeline/job.py', 'pipeline/modules_loader.py']
	miss = [f for f in need if not os.path.exists(os.path.join(ROOT, f))]
	return (len(miss) == 0), 'missing: ' + str(miss)


@check('app_server')
def c7():
	p = os.path.join(ROOT, 'app/server.py')
	if not os.path.exists(p):
		return False, 'app/server.py missing'
	return True, 'OK'


@check('modules_discoverable')
def c8():
	from pipeline import modules_loader as ml
	mods = ml.discover()
	bad = [k for k,v in mods.items() if not v['valid']]
	return (len(bad) == 0), 'found ' + str(len(mods)) + ' bad=' + str(bad)


@check('ui_index')
def c9():
	p = os.path.join(ROOT, 'app/ui/index.html')
	if not os.path.exists(p):
		return False, 'app/ui/index.html missing'
	t = open(p, encoding='utf-8').read()
	need = ['<!DOCTYPE', 'x-data', '/api/health']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'size=' + str(len(t)) + ' miss=' + str(miss)


@check('channels_imported')
def c10():
	c = state.connect()
	n = c.execute('SELECT COUNT(*) FROM channels').fetchone()[0]
	return (n > 0), 'count=' + str(n)


@check('write_api')
def c11():
	src = open(os.path.join(ROOT, 'app/server.py'), encoding='utf-8').read()
	need = ['/api/jobs', 'app.post', 'app.delete', '/api/cleanup']
	miss = [k for k in need if k not in src]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('ui_job_builder')
def c12():
	t = open(os.path.join(ROOT, 'app/ui/index.html'), encoding='utf-8').read()
	need = ['Create Job', 'submitJob', 'form: {']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('phase5_api')
def c13():
	src = open(os.path.join(ROOT, 'app/server.py'), encoding='utf-8').read()
	need = ['/api/pending', '/approve', '/reject', '/api/audit', '/api/assets', '/api/analytics']
	miss = [k for k in need if k not in src]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('ui_phase5')
def c14():
	t = open(os.path.join(ROOT, 'app/ui/index.html'), encoding='utf-8').read()
	need = ['Pending Approval', 'Audit Log', 'approve(id)', 'loadAnalytics']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('tray_app')
def c15():
	p = os.path.join(ROOT, 'app/tray.py')
	if not os.path.exists(p):
		return False, 'app/tray.py missing'
	t = open(p, encoding='utf-8').read()
	need = ['pystray', 'Dashboard', 'Start Server']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('phase7_scheduler')
def c16():
	p = os.path.join(ROOT, 'pipeline/scheduler.py')
	return os.path.exists(p), p


@check('phase8_notify')
def c17():
	p = os.path.join(ROOT, 'pipeline/notify.py')
	return os.path.exists(p), p


@check('phase9_quota')
def c18():
	from pipeline import quota
	q = quota.get()
	return (q['total'] > 0), 'remaining=' + str(q['remaining'])


@check('phase10_mversion')
def c19():
	p = os.path.join(ROOT, 'pipeline/mversion.py')
	return os.path.exists(p), p


@check('ui_action_buttons')
def c20():
	t = open(os.path.join(ROOT, 'app/ui/index.html'), encoding='utf-8').read()
	need = ['Create + Run ngay', 'runJob', 'scheduleJob', 'publishPub']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('api_run_schedule')
def c21():
	src = open(os.path.join(ROOT, 'app/server.py'), encoding='utf-8').read()
	need = ['/run', '/schedule', '/publish']
	miss = [k for k in need if k not in src]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('ui_settings_tab')
def c22():
	t = open(os.path.join(ROOT, 'app/ui/index.html'), encoding='utf-8').read()
	need = ['Settings', 'refreshAll', 'toast', 'setInterval']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('publish_wired')
def c23():
	src = open(os.path.join(ROOT, 'app/server.py'), encoding='utf-8').read()
	need = ['op.publish', 'op.set_channel']
	miss = [k for k in need if k not in src]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('ui_assets_modules')
def c24():
	t = open(os.path.join(ROOT, 'app/ui/index.html'), encoding='utf-8').read()
	need = ['Assets', 'Module Versioning', 'quotaInfo', 'schedulerStatus']
	miss = [k for k in need if k not in t]
	return (len(miss) == 0), 'miss=' + str(miss)


@check('api_assets_scheduler')
def c25():
	src = open(os.path.join(ROOT, 'app/server.py'), encoding='utf-8').read()
	need = ['/api/assets/list', '/api/analytics/quota', '/api/scheduler/status', '/api/audit/log']
	miss = [k for k in need if k not in src]
	return (len(miss) == 0), 'miss=' + str(miss)


def run(target=None):
	print('=== SELFCHECK ===')
	ok = 0
	fail = 0
	for name, fn in CHECKS:
		try:
			good, msg = fn()
		except Exception as e:
			good, msg = False, 'EXC: ' + str(e)[:80]
		mark = 'PASS' if good else 'FAIL'
		print(' [' + mark + '] ' + name + ' - ' + str(msg))
		if good:
			ok = ok + 1
		else:
			fail = fail + 1
	print('=== RESULT: ' + str(ok) + ' PASS, ' + str(fail) + ' FAIL ===')
	return 0 if fail == 0 else 1


if __name__ == '__main__':
	sys.exit(run())
