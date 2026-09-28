# -- coding: utf-8 --
# app/server.py - FastAPI read-only API (Phase 2)
import os, sys, json, time, shutil
try:
	from ops import _no_window # noqa
except Exception:
	pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pipeline import state
if os.environ.get('TNT_TEST_DB'):
	state.DB = os.environ['TNT_TEST_DB']
ROOT = os.environ.get('TNT_TEST_ROOT') or ROOT
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title='TNT Media API', version='0.1.0')

try:
	from app._routes_publish import router as _pub_router
	app.include_router(_pub_router)
except Exception as _e:
	print("[server] publish router FAIL:", str(_e)[:200])

try:
	from app._routes_prompts import router as _prompt_router
	app.include_router(_prompt_router)
except Exception as _e:
	print("[server] prompts router FAIL:", str(_e)[:200])

@app.get('/')
def root():
	return RedirectResponse(url='/ui/index.html')

from fastapi.staticfiles import StaticFiles as SF
UI = os.path.join(ROOT, 'app', 'ui')
if os.path.isdir(UI):
	app.mount('/ui', SF(directory=UI), name='ui')


@app.get('/api/health')
def health():
	c = state.connect()
	pubs = c.execute('SELECT COUNT() FROM publications').fetchone()[0]
	jobs = c.execute('SELECT COUNT() FROM jobs').fetchone()[0]
	sched_err = {}
	status_path = os.path.join(ROOT, 'state', 'scheduler_status.json')
	try:
		if os.path.exists(status_path):
			st = json.load(open(status_path, encoding='utf-8'))
			alive = bool(st.get('alive'))
			last_tick = st.get('last_tick') or ''
			stale = False
			try:
				import datetime as _dt
				lt = _dt.datetime.fromisoformat(last_tick) if last_tick else None
				stale = (lt is None) or ((_dt.datetime.now() - lt).total_seconds() > 180)
			except Exception:
				stale = True
			sched_err = {'alive': alive, 'stale': stale, 'last_tick': last_tick, 'last_error': st.get('last_error') or {}, 'pid': st.get('pid')}
		else:
			sched_err = {'alive': False, 'stale': True, 'last_tick': '', 'last_error': {}, 'pid': None}
	except Exception as _e:
		sched_err = {'alive': False, 'error': str(_e)[:120]}
	return {'ok': True, 'app': 'TNT Media OS', 'version': '0.2.0', 'publications': pubs, 'jobs': jobs, 'db': state.DB, 'scheduler_error': sched_err}


CONFIG_PATH = os.environ.get('TNT_TEST_CONFIG') or os.path.join(ROOT, 'state', 'ui_config.json')


@app.get('/api/config')
def get_ui_config():
	if os.path.exists(CONFIG_PATH):
		try:
			return json.load(open(CONFIG_PATH, encoding='utf-8'))
		except Exception:
			pass
	return {'publish_mode': 'approve'}


@app.post('/api/config')
def set_ui_config(payload: dict):
	cur = {}
	if os.path.exists(CONFIG_PATH):
		try:
			cur = json.load(open(CONFIG_PATH, encoding='utf-8'))
		except Exception:
			cur = {}
	if payload and 'publish_mode' in payload:
		cur['publish_mode'] = payload['publish_mode']
	os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
	json.dump(cur, open(CONFIG_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
	return {'ok': True, 'config': cur}

@app.get('/api/media/preview/{pub_id}')
def media_preview(pub_id: int):
	from fastapi.responses import FileResponse
	c = state.connect()
	row = c.execute('SELECT file_path FROM publications WHERE id=?', (pub_id,)).fetchone()
	if not row or not row['file_path']:
		return JSONResponse({'ok': False, 'error': 'no file'}, status_code=404)
	fp = os.path.abspath(row['file_path'])
	test_out = os.environ.get('TNT_TEST_OUTPUT'); allowed = ([os.path.abspath(test_out)] if test_out else [os.path.abspath(os.path.join(ROOT, 'output')), os.path.abspath(os.path.join(ROOT, 'work'))])
	if not any(fp.startswith(a + os.sep) or fp == a for a in allowed):
		return JSONResponse({'ok': False, 'error': 'path not allowed'}, status_code=403)
	if not os.path.exists(fp):
		return JSONResponse({'ok': False, 'error': 'file missing'}, status_code=404)
	return FileResponse(fp, media_type='video/mp4')

@app.get('/api/channels')
def channels():
	c = state.connect()
	rows = c.execute('SELECT id, enabled FROM channels').fetchall()
	return {'channels': [dict(r) for r in rows]}


@app.get('/api/publications')
def publications(limit: int = 50, channel_id: str = None):
	c = state.connect()
	if channel_id:
		rows = c.execute('SELECT id, channel_id, kind, youtube_id, status, published_at FROM publications WHERE channel_id=? LIMIT ?', (channel_id, limit)).fetchall()
	else:
		rows = c.execute('SELECT id, channel_id, kind, youtube_id, status, published_at FROM publications ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
	return {'items': [dict(r) for r in rows]}


@app.get('/api/jobs')
def jobs(limit: int = 50):
	import time as _t
	c = state.connect()
	rows = c.execute('SELECT id, channel_id, kind, status, created_at FROM jobs ORDER BY created_at DESC LIMIT ?', (limit,)).fetchall()
	now = _t.time()
	out = []
	for r in rows:
		d = dict(r)
		d['log_tail'] = []
		d['elapsed_sec'] = 0
		try:
			ca = d.get('created_at')
			if ca:
				import datetime as _dt
				t0 = _dt.datetime.strptime(ca, '%Y-%m-%dT%H:%M:%S').timestamp()
				d['elapsed_sec'] = int(now - t0)
		except Exception:
			pass
		lg = os.path.join(ROOT, 'logs', 'runner_' + str(d.get('id')) + '.log')
		if os.path.exists(lg):
			try:
				d['log_tail'] = open(lg, encoding='utf-8', errors='replace').read().splitlines()[-2:]
			except Exception:
				pass
		out.append(d)
	return {'items': out}


@app.get('/api/quota')
def quota():
	c = state.connect()
	rows = c.execute('SELECT account, date, units_used, units_total FROM quota ORDER BY date DESC LIMIT 10').fetchall()
	return {'items': [dict(r) for r in rows]}


@app.get('/api/modules')
def modules():
	from pipeline import modules_loader as ml
	mods = ml.discover()
	return {'items': [{'name': k, 'version': v['meta'].get('version'), 'valid': v['valid'], 'category': v['category']} for k, v in mods.items()]}



@app.post('/api/jobs')
def create_job(payload: dict):
	from pipeline import job as jobmod
	try:
		j = jobmod.Job.from_dict(payload)
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=400)
	errs = j.validate()
	if errs:
		return JSONResponse({'ok': False, 'errors': errs}, status_code=400)
	c = state.init()
	c.execute('INSERT INTO jobs (id, channel_id, topic, kind, length_override, voice_override, music_mood, count, require_approval, run_at, repeat, status, priority, created_by, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (j.job_id, j.channel_id, j.topic, j.kind, j.length_override, j.voice_override, j.music_mood, j.count, int(j.require_approval), j.run_at, j.repeat, 'pending', j.priority, j.created_by, state.now(), state.now()))
	c.commit()
	return {'ok': True, 'job_id': j.job_id}


@app.delete('/api/jobs/{job_id}')
def delete_job(job_id: str):
	c = state.init()
	r = c.execute('DELETE FROM jobs WHERE id=?', (job_id,))
	c.commit()
	return {'ok': r.rowcount > 0, 'deleted': r.rowcount}


@app.post('/api/cleanup')
def cleanup(force: bool = False):
	import subprocess
	cmd = [sys.executable, os.path.join(ROOT, 'ops', 'publish_cleanup.py')]
	if force:
		cmd.append('--force')
	try:
		r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, creationflags=0x08000000)
		return {'ok': r.returncode == 0, 'stdout': r.stdout[-500:], 'stderr': r.stderr[-200:]}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)


@app.get('/api/pending')
def pending():
	c = state.connect()
	rows = c.execute('SELECT id, channel_id, kind, topic, file_path, created_at FROM publications WHERE status=? ORDER BY id DESC', ('rendered',)).fetchall()
	return {'items': [dict(r) for r in rows]}


@app.post('/api/publications/{pub_id}/approve')
def approve(pub_id: int):
	c = state.init()
	r = c.execute('UPDATE publications SET status=? WHERE id=? AND status=?', ('approved', pub_id, 'rendered'))
	c.commit()
	return {'ok': r.rowcount > 0, 'approved': r.rowcount}


@app.post('/api/publications/{pub_id}/reject')
def reject(pub_id: int, reason: str = ''):
	c = state.init()
	r = c.execute('UPDATE publications SET status=? WHERE id=? AND status=?', ('rejected', pub_id, 'rendered'))
	c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'reject', str(pub_id), reason[:200], state.now()))
	c.commit()
	return {'ok': r.rowcount > 0, 'rejected': r.rowcount}


@app.get('/api/audit')
def audit(limit: int = 50):
	c = state.connect()
	rows = c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
	return {'items': [dict(r) for r in rows]}


@app.get('/api/assets')
def assets(kind: str = None):
	c = state.connect()
	if kind:
		rows = c.execute('SELECT * FROM assets WHERE kind=? AND enabled=1', (kind,)).fetchall()
	else:
		rows = c.execute('SELECT * FROM assets WHERE enabled=1').fetchall()
	return {'items': [dict(r) for r in rows]}


@app.get('/api/analytics')
def analytics():
	c = state.connect()
	total = c.execute('SELECT COUNT() FROM publications').fetchone()[0]
	by_ch = c.execute('SELECT channel_id, COUNT() FROM publications GROUP BY channel_id').fetchall()
	by_status = c.execute('SELECT status, COUNT(*) FROM publications GROUP BY status').fetchall()
	return {'total': total, 'by_channel': [dict(zip([chr(99)+chr(104),chr(110)], r)) for r in by_ch], 'by_status': [dict(zip([chr(115),chr(110)], r)) for r in by_status]}


@app.post('/api/jobs/{job_id}/run')
def run_job(job_id: str, dry_run: bool = False):
	import subprocess
	c = state.connect()
	row = c.execute('SELECT id, channel_id, kind, topic, length_override, voice_override, music_mood, count, require_approval FROM jobs WHERE id=?', (job_id,)).fetchone()
	if not row:
		return JSONResponse({'ok': False, 'error': 'job not found'}, status_code=404)
	job_dict = {'job_id': row['id'], 'channel_id': row['channel_id'], 'kind': row['kind'], 'topic': row['topic'], 'length_override': row['length_override'], 'voice_override': row['voice_override'], 'music_mood': row['music_mood'], 'count': row['count'], 'require_approval': bool(row['require_approval']), 'created_by': 'ui'}
	cmd = [sys.executable, '-m', 'pipeline.runner', '--job-json', json.dumps(job_dict, ensure_ascii=False)]
	if dry_run:
		cmd.append('--dry-run')
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	log = os.path.join(ROOT, 'logs', 'runner' + job_id + '.log')
	os.makedirs(os.path.dirname(log), exist_ok=True)
	f = open(log, 'w')
	subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	return {'ok': True, 'job_id': job_id, 'log': log}


@app.post('/api/jobs/{job_id}/schedule')
def schedule_job(job_id: str, run_at: str = ''):
	c = state.init()
	r = c.execute('UPDATE jobs SET run_at=?, status=? WHERE id=?', (run_at, 'scheduled', job_id))
	c.commit()
	return {'ok': r.rowcount > 0, 'run_at': run_at}


@app.get('/api/topics')
def topics(channel_id: str = None):
	c = state.connect()
	if channel_id:
		rows = c.execute('SELECT * FROM topics WHERE channel_id=? ORDER BY score DESC', (channel_id,)).fetchall()
	else:
		rows = c.execute('SELECT * FROM topics ORDER BY score DESC LIMIT 200').fetchall()
	return {'items': [dict(r) for r in rows]}


@app.post('/api/topics')
def add_topic(payload: dict):
	c = state.init()
	ch = payload.get('channel_id')
	kd = payload.get('kind', '')
	tp = payload.get('topic', '')
	sc = payload.get('score', 0)
	c.execute('INSERT OR REPLACE INTO topics (channel_id, kind, topic, source, score, created_at) VALUES (?,?,?,?,?,?)', (ch, kd, tp, 'manual', sc, state.now()))
	c.commit()
	return {'ok': True}


@app.delete('/api/topics/{tid}')
def del_topic(tid: int):
	c = state.init()
	r = c.execute('DELETE FROM topics WHERE id=?', (tid,))
	c.commit()
	return {'ok': r.rowcount > 0}


@app.get('/api/trends')
def trends(limit: int = 30):
	c = state.connect()
	rows = c.execute('SELECT * FROM trends ORDER BY ts DESC LIMIT ?', (limit,)).fetchall()
	return {'items': [dict(r) for r in rows]}


@app.post('/api/idea')
def idea(payload: dict):
	sd = (payload.get('seed') or '').strip()
	if not sd:
		return {'items': []}
	hooks = [sd + ' - su that bat ngo?', sd + ' - dieu ban chua biet', sd + ' - goc nhin khac', sd + ' - tai sao lai vay?']
	return {'items': hooks}


@app.get('/api/config/voices')
def voices():
	return {'items': ['HoaiMy', 'NamMinh', 'HoaiMyNeural', 'NamMinhNeural']}


@app.get('/api/config/kinds')
def kinds(channel_id: str = None):
	import json as j
	CH = os.path.join(ROOT, 'channels')
	out = set()
	if channel_id:
		fp = os.path.join(CH, channel_id + '.json')
		if os.path.exists(fp):
			d = j.load(open(fp, encoding='utf-8'))
			out.update(d.get('topics', []))
	else:
		for f in os.listdir(CH):
			if f.endswith('.json') and 'template' not in f:
				try:
					d = j.load(open(os.path.join(CH, f), encoding='utf-8'))
					out.update(d.get('topics', []))
				except Exception:
					pass
	return {'items': sorted(out)}


@app.get('/api/diagnostics/selfcheck')
def diag_selfcheck():
	import subprocess
	try:
		r = subprocess.run([sys.executable, '-m', 'pipeline.selfcheck'], capture_output=True, text=True, cwd=ROOT, timeout=90, creationflags=0x08000000)
		return {'ok': r.returncode == 0, 'output': r.stdout[-2500:]}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)


@app.get('/api/diagnostics/logs')
def diag_logs(name: str = 'notify.log', limit: int = 100):
	p = os.path.join(ROOT, 'logs', os.path.basename(name))
	if not os.path.exists(p):
		return {'items': [], 'note': 'no log file'}
	lines = open(p, encoding='utf-8', errors='replace').read().splitlines()
	return {'items': lines[-limit:]}


@app.get('/api/diagnostics/logs/list')
def diag_loglist():
	d = os.path.join(ROOT, 'logs')
	if not os.path.isdir(d):
		return {'items': []}
	out = []
	for f in sorted(os.listdir(d)):
		fp = os.path.join(d, f)
		if os.path.isfile(fp):
			out.append({'name': f, 'size': os.path.getsize(fp)})
	return {'items': out[-30:]}


@app.post('/api/killswitch')
def killswitch():
	c = state.init()
	r = c.execute('UPDATE jobs SET status=? WHERE status IN (?,?)', ('cancelled', 'pending', 'running'))
	n = r.rowcount
	c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'killswitch', 'all', 'manual stop', state.now()))
	c.commit()
	return {'ok': True, 'cancelled': n}


@app.post('/api/backup')
def backup():
	from ops import backup_state as _bs
	bk = os.path.join(ROOT, 'state', 'backup')
	try:
		dst = _bs.backup_sqlite(state.DB, bk)
		return {'ok': True, 'file': os.path.basename(dst), 'bytes': os.path.getsize(dst)}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)

@app.get('/api/backup/list')
def backup_list():
	bk = os.path.join(ROOT, 'state', 'backup')
	if not os.path.isdir(bk):
		return {'items': []}
	out = []
	for f in sorted(os.listdir(bk)):
		fp = os.path.join(bk, f)
		out.append({'name': f, 'size': os.path.getsize(fp), 'mtime': os.path.getmtime(fp)})
	return {'items': out[-20:]}


@app.get('/api/modules/versions')
def mod_versions(name: str = None):
	from pipeline import mversion
	return {'items': mversion.list_versions(name)}


@app.post('/api/modules/snapshot')
def mod_snapshot(payload: dict):
	from pipeline import mversion
	p = payload.get('path')
	v = payload.get('version', 'manual')
	if not p:
		return JSONResponse({'ok': False, 'error': 'path required'}, status_code=400)
	full = os.path.join(ROOT, p)
	try:
		dst = mversion.snapshot(full, v, payload.get('note', ''))
		return {'ok': True, 'snapshot': os.path.basename(dst)}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)


@app.post('/api/modules/rollback')
def mod_rollback(payload: dict):
	from pipeline import mversion
	p = payload.get('path')
	v = payload.get('version')
	if not p or not v:
		return JSONResponse({'ok': False, 'error': 'path + version required'}, status_code=400)
	full = os.path.join(ROOT, p)
	return mversion.rollback(full, v)


@app.get('/api/assets/list')
def assets_list(kind=None):
	out = []
	for d in ['music_bank', 'assets']:
		fp = os.path.join(ROOT, d)
		if os.path.isdir(fp):
			for f in sorted(os.listdir(fp))[:200]:
				if f.endswith(('.mp3', '.wav', '.m4a')):
					out.append({'dir': d, 'name': f, 'size': os.path.getsize(os.path.join(fp, f))})
	return {'items': out[:300], 'total': len(out)}


@app.get('/api/analytics/quota')
def analytics_quota():
	from pipeline import quota
	return quota.get()


@app.get('/api/analytics/feedback')
def analytics_feedback():
	c = state.connect()
	rows = c.execute('SELECT topic, COUNT(*) AS n, SUM(view_count) AS views FROM publications WHERE topic IS NOT NULL GROUP BY topic ORDER BY views DESC LIMIT 20').fetchall()
	return {'items': [dict(r) for r in rows]}


@app.get('/api/scheduler/status')
def scheduler_status():
	import json as j
	c = state.connect()
	rows = c.execute('SELECT id, schedule FROM channels WHERE enabled=1').fetchall()
	out = []
	for r in rows:
		sched = {}
		try: sched = j.loads(r[1] or '')
		except Exception: pass
		out.append({'channel': r[0], 'cron': sched.get('cron')})
	return {'items': out}


@app.post('/api/channels/{cid}/cron')
def set_cron(cid: str, payload: dict):
	import json as j
	c = state.init()
	cron = payload.get('cron', '')
	row = c.execute('SELECT schedule FROM channels WHERE id=?', (cid,)).fetchone()
	sched = {}
	if row and row[0]:
		try: sched = j.loads(row[0])
		except Exception: sched = {}
	sched['cron'] = cron
	c.execute('UPDATE channels SET schedule=?, updated_at=? WHERE id=?', (j.dumps(sched), state.now(), cid))
	c.commit()
	return {'ok': True, 'cron': cron}


@app.get('/api/audit/log')
def audit_log(action=None, limit=100):
	c = state.connect()
	if action:
		rows = c.execute('SELECT * FROM audit WHERE action=? ORDER BY id DESC LIMIT ?', (action, limit)).fetchall()
	else:
		rows = c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
	return {'items': [dict(r) for r in rows]}



def main():
	import uvicorn
	uvicorn.run(app, host='127.0.0.1', port=7777)


if __name__ == '__main__':
	main()
