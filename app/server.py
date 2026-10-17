# -- coding: utf-8 --
# app/server.py - FastAPI read-only API (Phase 2)
import os, sys, json, time, shutil
try:
	from ops import _no_window # noqa
except Exception:
	pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from fastapi import FastAPI, Request, HTTPException
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

try:
	from app._routes_analyze import router as _analyze_router
	app.include_router(_analyze_router)
except Exception as _e:
	print("[server] analyze router FAIL:", str(_e)[:200])

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

@app.post('/api/channels')
def channel_create(req: Request):
	body = None
	try:
		import asyncio
		body = asyncio.run(req.json())
	except Exception:
		body = {}
	if not isinstance(body, dict):
		body = {}
	cid = (body.get('id') or '').strip()
	if not cid:
		raise HTTPException(status_code=400, detail='id required')
	c = state.connect()
	row = c.execute('SELECT id FROM channels WHERE id=?', (cid,)).fetchone()
	if row:
		c.close()
		raise HTTPException(status_code=409, detail='exists')
	sql = 'INSERT INTO channels (id, enabled, niche, kinds, voice, max_length_sec, style, publish_mode, quality_gate) VALUES (?,?,?,?,?,?,?,?,?)'
	vals = (cid, int(body.get('enabled', 1)), body.get('niche', ''), body.get('kinds', 'short'), body.get('voice', ''), int(body.get('max_length_sec', 60)), body.get('style', ''), body.get('publish_mode', 'approve'), body.get('quality_gate', 'normal'))
	c.execute(sql, vals)
	c.commit()
	c.close()
	return {'ok': True, 'id': cid}


@app.delete('/api/channels/{cid}')
def channel_delete(cid: str):
	c = state.connect()
	c.execute('DELETE FROM channels WHERE id=?', (cid,))
	c.commit()
	c.close()
	return {'ok': True}

@app.get('/api/channels')
def channels():
	c = state.connect()
	rows = c.execute('SELECT id, enabled FROM channels').fetchall()
	out = []
	for r in rows:
		d = dict(r)
		d['token'] = False
		try:
			from ops import channel_loader as chl
			cfg = chl.load(r['id'])
			tp = chl.token_path(cfg)
			d['token'] = bool(tp and os.path.exists(tp))
		except Exception:
			pass
		out.append(d)
	return {'channels': out}


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
		lg = os.path.join(ROOT, 'logs', 'runner' + str(d.get('id')) + '.log')
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


@app.get('/api/modules/info')
def modules_info():
	import json
	p = os.path.join(ROOT, 'module_registry.json')
	if not os.path.exists(p):
		return {'items': []}
	try:
		d = json.load(open(p, encoding='utf-8'))
		return {'items': d}
	except Exception as e:
		return {'items': {}, 'err': str(e)[:150]}

@app.get('/api/modules')
def modules():
	from pipeline import modules_loader as ml
	mods = ml.discover()
	import json as _json
	reg = {}
	try:
		rp = os.path.join(ROOT, 'module_registry.json')
		if os.path.exists(rp):
			reg = _json.load(open(rp, encoding='utf-8'))
	except Exception:
		reg = {}
	items = []
	for k, v in mods.items():
		r = reg.get(k, {}) or {}
		if not r.get('visible', False):
			continue
		items.append({
			'name': k,
			'version': v['meta'].get('version'),
			'valid': v['valid'],
			'category': v['category'],
			'title': r.get('title', ''),
			'desc': r.get('mech', ''),
			'when_to_use': r.get('when', ''),
			'strength': r.get('strength', ''),
			'free': r.get('free', True),
			'note': r.get('note', ''),
		})
	return {'items': items}



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
	import json as _j
	mod_json = _j.dumps(j.modules or {}, ensure_ascii=False)
	c.execute('INSERT INTO jobs (id, channel_id, topic, kind, length_override, voice_override, voice_preset, music_mood, count, require_approval, run_at, repeat, status, priority, created_by, created_at, updated_at, modules) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (j.job_id, j.channel_id, j.topic, j.kind, j.length_override, j.voice_override, j.voice_preset, j.music_mood, j.count, int(j.require_approval), j.run_at, j.repeat, 'pending', j.priority, j.created_by, state.now(), state.now(), mod_json))
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
def approve(pub_id: int, upload: bool = True):
	c = state.init()
	row = c.execute('SELECT id, channel_id, title, file_path, status FROM publications WHERE id=?', (pub_id,)).fetchone()
	if not row:
		return JSONResponse({'ok': False, 'error': 'not found'}, status_code=404)
	if row['status'] not in ('rendered', 'approved'):
		return JSONResponse({'ok': False, 'error': 'status=' + str(row['status'])}, status_code=400)
	vid = None
	err = None
	if upload:
		try:
			from ops import os_publish as _op
			ttl = row['title'] or ('Video ' + str(pub_id))
			res = _op.publish(row['file_path'], ttl, '', force=False)
			vid = res.get('youtube_id') or res.get('id') or res.get('video_id')
		except Exception as e:
			err = str(e)[:200]
	if vid:
		c.execute('UPDATE publications SET status=?, youtube_id=?, published_at=? WHERE id=?', ('published', vid, state.now(), pub_id))
		c.commit()
		return {'ok': True, 'published': True, 'youtube_id': vid}
	if err:
		return JSONResponse({'ok': False, 'error': err}, status_code=500)
	r = c.execute('UPDATE publications SET status=? WHERE id=? AND status=?', ('approved', pub_id, 'rendered'))
	c.commit()
	return {'ok': True, 'approved': r.rowcount, 'note': 'no upload (token missing?)'}


@app.post('/api/publications/{pub_id}/reject')
def reject(pub_id: int, reason: str = ''):
	c = state.init()
	r = c.execute('UPDATE publications SET status=? WHERE id=? AND status=?', ('rejected', pub_id, 'rendered'))
	c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'reject', str(pub_id), reason[:200], state.now()))
	c.commit()
	return {'ok': r.rowcount > 0, 'rejected': r.rowcount}




@app.get('/api/publications/queue')
def publications_queue(status: str = None, channel_id: str = None, limit: int = 100):
	c = state.connect()
	sql = "SELECT id, job_id, channel_id, kind, topic, title, file_path, status, schedule_at, created_at, engine_used, provider FROM publications WHERE status IN ('rendered','scheduled','approved')"
	params = []
	if status:
		sql += ' AND status=?'
		params.append(status)
	if channel_id:
		sql += ' AND channel_id=?'
		params.append(channel_id)
	sql += ' ORDER BY CASE WHEN schedule_at IS NULL THEN 0 ELSE 1 END, schedule_at ASC, created_at DESC LIMIT ?'
	params.append(limit)
	rows = c.execute(sql, tuple(params)).fetchall()
	c.close()
	return {'items': [dict(r) for r in rows]}


@app.post('/api/publications/{pub_id}/publish')
def publish_pub(pub_id: int):
	return approve(pub_id, upload=True)


@app.post('/api/publications/{pub_id}/schedule')
def schedule_pub(pub_id: int, payload: dict = None):
	c = state.init()
	row = c.execute('SELECT id, status, schedule_at FROM publications WHERE id=?', (pub_id,)).fetchone()
	if not row:
		c.close()
		return JSONResponse({'ok': False, 'error': 'not found'}, status_code=404)
	if row['status'] not in ('rendered', 'scheduled', 'approved'):
		c.close()
		return JSONResponse({'ok': False, 'error': 'status=' + str(row['status'])}, status_code=400)
	at = (payload or {}).get('at') or (payload or {}).get('schedule_at')
	if not at:
		c.close()
		return JSONResponse({'ok': False, 'error': 'at required (YYYY-MM-DD HH:MM)'}, status_code=400)
	c.execute('UPDATE publications SET status=?, schedule_at=? WHERE id=?', ('scheduled', at, pub_id))
	c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'schedule', str(pub_id), at[:200], state.now()))
	c.commit()
	c.close()
	return {'ok': True, 'id': pub_id, 'schedule_at': at}


@app.post('/api/publications/{pub_id}/unschedule')
def unschedule_pub(pub_id: int):
	c = state.init()
	r = c.execute('UPDATE publications SET status=?, schedule_at=NULL WHERE id=? AND status=?', ('rendered', pub_id, 'scheduled'))
	c.commit()
	c.close()
	return {'ok': r.rowcount > 0}





@app.post('/api/publications/bulk_publish')
def bulk_publish(payload: dict):
	ids = (payload or {}).get('ids') or []
	if not ids:
		return JSONResponse({'ok': False, 'error': 'ids required'}, status_code=400)
	results = []
	for pid in ids:
		try:
			r = publish_pub(int(pid))
			if isinstance(r, dict):
				results.append({'id': pid, 'ok': r.get('ok', False), 'result': r.get('youtube_id')})
			else:
				results.append({'id': pid, 'ok': True})
		except Exception as e:
			results.append({'id': pid, 'ok': False, 'error': str(e)[:120]})
	ok_count = sum(1 for x in results if x.get('ok'))
	return {'ok': True, 'count': ok_count, 'total': len(ids), 'results': results}


@app.post('/api/publications/bulk_schedule')
def bulk_schedule(payload: dict):
	ids = (payload or {}).get('ids') or []
	at = (payload or {}).get('at')
	if not ids or not at:
		return JSONResponse({'ok': False, 'error': 'ids + at required'}, status_code=400)
	c = state.init()
	ok_count = 0
	for pid in ids:
		try:
			r = c.execute('UPDATE publications SET status=?, schedule_at=? WHERE id=? AND status IN (?,?,?)', ('scheduled', at, int(pid), 'rendered', 'scheduled', 'publish_failed'))
			if r.rowcount:
				ok_count += 1
		except Exception:
			pass
	c.commit()
	c.close()
	return {'ok': True, 'count': ok_count, 'total': len(ids), 'at': at}


@app.post('/api/publications/{pub_id}/update')
def update_pub(pub_id: int, payload: dict):
	c = state.init()
	row = c.execute('SELECT id FROM publications WHERE id=?', (pub_id,)).fetchone()
	if not row:
		c.close()
		return JSONResponse({'ok': False, 'error': 'not found'}, status_code=404)
	fields = []
	vals = []
	for k in ('title', 'topic'):
		if k in (payload or {}):
			fields.append(k + '=?')
			vals.append((payload or {}).get(k))
	if not fields:
		c.close()
		return {'ok': False, 'error': 'no fields'}
	vals.append(pub_id)
	c.execute('UPDATE publications SET ' + ', '.join(fields) + ' WHERE id=?', tuple(vals))
	c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'update_meta', str(pub_id), str(list(payload.keys())), state.now()))
	c.commit()
	c.close()
	return {'ok': True, 'id': pub_id}




@app.get('/api/ai/suggest/{pub_id}')
def ai_suggest(pub_id: int):
	try:
		from pipeline import ai_advisor as ai
		return ai.suggest_metadata(pub_id)
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:150]}, status_code=500)


@app.get('/api/ai/score/{pub_id}')
def ai_score(pub_id: int):
	try:
		from pipeline import ai_advisor as ai
		return ai.score_video(pub_id)
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:150]}, status_code=500)


@app.get('/api/ai/feedback')
def ai_feedback(channel_id: str = None):
	try:
		from pipeline import ai_advisor as ai
		return ai.feedback_report(channel_id)
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:150]}, status_code=500)




@app.get('/api/publications/{pub_id}/thumb')
def pub_thumb(pub_id: int):
	from fastapi.responses import FileResponse
	c = state.connect()
	row = c.execute('SELECT file_path FROM publications WHERE id=?', (pub_id,)).fetchone()
	c.close()
	if not row or not row['file_path']:
		return JSONResponse({'ok': False, 'error': 'no file'}, status_code=404)
	try:
		from pipeline import thumb_cache as tc
		tp = tc.get_thumb(row['file_path'])
		if tp and os.path.exists(tp):
			return FileResponse(tp, media_type='image/jpeg')
	except Exception as e:
		pass
	return JSONResponse({'ok': False, 'error': 'thumb fail'}, status_code=404)




@app.get('/api/dashboard/stats')
def dash_stats():
	try:
		from pipeline import dash_stats as ds
		return {'ok': True, 'days': ds.views_by_day(7), 'summary': ds.summary()}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)




@app.post('/api/channels/{cid}/update')
def channel_update(cid: str, payload: dict):
	try:
		from ops import channel_loader as chl
		cfg = chl.load(cid)
		for k in ('niche', 'kinds', 'voice', 'max_length_sec', 'publish_mode', 'enabled'):
			if k in (payload or {}):
				cfg[k] = (payload or {}).get(k)
		if 'style' in (payload or {}):
			st = cfg.get('style') or {}
			if isinstance(st, dict):
				st.update(payload['style'])
			cfg['style'] = st
		chl.save(cid, cfg)
		return {'ok': True, 'id': cid}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)


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


@app.get('/api/jobs/{job_id}')
def job_detail(job_id: str):
	c = state.connect()
	sql = 'SELECT id, channel_id, kind, topic, status, created_at, count FROM jobs WHERE id=?'
	row = c.execute(sql, (job_id,)).fetchone()
	if not row:
		c.close()
		return JSONResponse({'ok': False, 'err': 'not found'}, status_code=404)
	d = dict(row)
	lg = os.path.join(ROOT, 'logs', 'runner' + str(job_id) + '.log')
	tail = []
	if os.path.exists(lg):
		try:
			tail = open(lg, encoding='utf-8', errors='replace').read().splitlines()[-40:]
		except Exception:
			tail = []
	d['log_tail'] = tail
	st = str(d.get('status') or '')
	d['running'] = st in ('running', 'pending')
	c.close()
	return d

@app.post('/api/jobs/{job_id}/approve')
def job_approve(job_id: str):
	c = state.init()
	r = c.execute('UPDATE jobs SET status=?, updated_at=? WHERE id=? AND status=?', ('pending', state.now(), job_id, 'pending_approval'))
	c.commit()
	return {'ok': r.rowcount > 0, 'approved': r.rowcount}


@app.post('/api/jobs/approve_all')
def jobs_approve_all():
	c = state.init()
	r = c.execute('UPDATE jobs SET status=?, updated_at=? WHERE status=?', ('pending', state.now(), 'pending_approval'))
	c.commit()
	return {'ok': True, 'approved': r.rowcount}

@app.post('/api/jobs/{job_id}/run')
def run_job(job_id: str, dry_run: bool = False):
	import subprocess
	c = state.connect()
	row = c.execute('SELECT id, channel_id, kind, topic, length_override, voice_override, voice_preset, music_mood, count, require_approval, modules FROM jobs WHERE id=?', (job_id,)).fetchone()
	if not row:
		return JSONResponse({'ok': False, 'error': 'job not found'}, status_code=404)
	import json as _j2
	mod_data = {}
	try:
		if 'modules' in row.keys() and row['modules']:
			mod_data = _j2.loads(row['modules'])
	except Exception:
		mod_data = {}
	job_dict = {'job_id': row['id'], 'channel_id': row['channel_id'], 'kind': row['kind'], 'topic': row['topic'], 'length_override': row['length_override'], 'voice_override': row['voice_override'], 'voice_preset': (row['voice_preset'] if 'voice_preset' in row.keys() else None), 'music_mood': row['music_mood'], 'count': row['count'], 'require_approval': bool(row['require_approval']), 'created_by': 'ui', 'modules': mod_data}
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


@app.post('/api/trends/collect')
def trends_collect(payload: dict = None):
	try:
		from ops import trend_analyzer as ta
		p = payload or {}
		niche = p.get('niche') or p.get('kind')
		r = ta.run(limit=int(p.get('limit', 30)), niche=niche)
		return r
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}

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
	labels = {'female_north': 'HoaiMy (VN nữ Bắc)', 'male_north': 'NamMinh (VN nam Bắc)', 'female_multilingual': 'Ava (đa ngôn ngữ)', 'female_emma': 'Emma (đa ngôn ngữ)', 'female_jenny': 'Jenny (đa ngôn ngữ)', 'male_andrew': 'Andrew (đa ngôn ngữ)'}
	items = []
	try:
		from modules.voice import edge_tts as ev
		for k in ev.list_voices():
			items.append({'id': k, 'label': labels.get(k, k), 'voice': ev.VI_VOICES.get(k, '')})
	except Exception:
		items = [{'id': 'female_north', 'label': labels['female_north'], 'voice': 'vi-VN-HoaiMyNeural'}]
	return {'items': items}


@app.get('/api/config/presets')
def presets():
	labels = {'default': 'Mặc định', 'cheerful': 'Vui vẻ', 'sad': 'Buồn', 'excited': 'Hào hứng', 'calm': 'Điềm tĩnh', 'narrator': 'Kể chuyện', 'kids': 'Trẻ em', 'news': 'Tin tức'}
	items = []
	try:
		from modules.voice import edge_tts as ev
		for k in ev.list_presets():
			pv = ev.resolve_preset(k)
			items.append({'id': k, 'label': labels.get(k, k), 'rate': pv.get('rate'), 'pitch': pv.get('pitch'), 'volume': pv.get('volume')})
	except Exception:
		items = [{'id': 'default', 'label': 'Mac dinh'}]
	return {'items': items}


@app.get('/api/config/kinds')
def kinds(channel_id: str = None):
	import os
	out = []
	seen = set()
	if channel_id:
		try:
			from ops import channel_loader as chl
			cfg = chl.load(channel_id)
			kinds = (cfg.get('content') or {}).get('kinds') or []
			if isinstance(kinds, list):
				out = [str(k) for k in kinds]
		except Exception:
			pass
		return {'items': out}
	try:
		from ops import channel_loader as chl
		ch_dir = chl.channels_dir()
		if os.path.isdir(ch_dir):
			for name in sorted(os.listdir(ch_dir)):
				if name.startswith('_'):
					continue
				p = os.path.join(ch_dir, name, 'channel.json')
				if not os.path.exists(p):
					continue
				try:
					import json as j
					cfg = j.load(open(p, encoding='utf-8'))
					ks = (cfg.get('content') or {}).get('kinds') or []
					for k in ks:
						sk = str(k)
						if sk not in seen:
							seen.add(sk)
							out.append(sk)
				except Exception:
					pass
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


@app.post('/api/metrics/sync')
def metrics_sync():
	try:
		from ops import yt_metrics as ym
		return ym.sync_db()
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}


@app.get('/api/metrics/{pub_id}')
def metrics_get(pub_id: int):
	c = state.connect()
	r = c.execute('SELECT youtube_id, channel_id FROM publications WHERE id=?', (pub_id,)).fetchone()
	c.close()
	if not r or not r['youtube_id']:
		return {'ok': False, 'error': 'no youtube_id'}
	from ops import yt_metrics as ym
	return ym.get_metrics([r['youtube_id']], r['channel_id'])@app.post('/api/killswitch')
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


@app.get('/api/studio/history')
def studio_history(limit: int = 10):
	try:
		import os as _os, glob as _g, json as _j
		hd = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'state', 'studio_history')
		if not _os.path.isdir(hd):
			return {'ok': True, 'items': []}
		files = sorted(_g.glob(_os.path.join(hd, '*.json')), reverse=True)[:int(limit)]
		items = []
		for f in files:
			try:
				d = _j.loads(open(f, encoding='utf-8').read())
				items.append({'file': _os.path.basename(f), 'ts': d.get('ts'), 'summary': (d.get('advisor') or {}).get('summary', '')[:200], 'ideas': len((d.get('advisor') or {}).get('next_ideas', []))})
			except Exception:
				pass
		return {'ok': True, 'items': items}
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}

@app.get('/api/studio/advice')
def studio_advice(force: int = 0, channel_id: str = '', kind: str = ''):
	try:
		from ops import studio_advisor as sa
		return sa.analyze(channel_id=(channel_id or None), force=bool(force), kind=(kind or None))
	except Exception as e:
		return {'ok': False, 'error': str(e)[:300]}

@app.get('/api/studio/snapshot')
def studio_snapshot(channel_id: str = ''):
	try:
		from ops import studio_advisor as sa
		return sa.fetch_channel_snapshot(channel_id=(channel_id or None))
	except Exception as e:
		return {'ok': False, 'error': str(e)[:300]}

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




@app.get('/api/video/engines')
def video_engines():
	out = {}
	try:
		from modules.video.providers import PROVIDERS, provider_config
		for name in PROVIDERS:
			cfg = provider_config(name) or {}
			out[name] = {'available': bool(cfg.get('available')), 'tested': bool(cfg.get('tested')), 'free': True, 'model': cfg.get('model', '')}
	except Exception as e:
		out['_error'] = str(e)[:200]
	try:
		from modules.render import pexels_engine
		out['pexels'] = {'available': True, 'tested': True, 'free': True, 'model': 'stock-video'}
	except Exception as e:
		out['pexels'] = {'available': False}
	try:
		import urllib.request
		urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=2)
		out['flow'] = {'available': True, 'tested': True, 'free': True, 'model': 'veo'}
	except Exception:
		out['flow'] = {'available': False}
	try:
		from ops import ffmpeg_render
		out['ffmpeg'] = {'available': True, 'tested': True, 'free': True, 'model': 'local-ffmpeg'}
	except Exception:
		out['ffmpeg'] = {'available': False}
	out['gacha'] = {'available': True, 'tested': True, 'free': True, 'model': 'gacha-anime'}
	try:
		from modules.render import quote_engine as _qe
		out['quote'] = {'available': True, 'tested': True, 'free': True, 'model': 'quote-engine', 'note': 'Flow(primary) -> Pexels(fallback), full-free'}
		out['quote_v2'] = {'available': True, 'tested': True, 'free': True, 'model': 'quote-pipeline-v1', 'note': 'mix+compose+boost+vn_guard'}
	except Exception:
		out['quote'] = {'available': False}
	return {'ok': True, 'engines': out, 'generated_by': 'TNT Media OS'}


@app.post('/api/video/generate')
def video_generate(payload: dict):
	import time as tnttm
	prompt = (payload.get('prompt') or '').strip()
	if not prompt:
		return JSONResponse({'ok': False, 'error': 'prompt required'}, status_code=400)
	engine = (payload.get('engine') or 'auto').lower()
	duration = int(payload.get('duration') or 8)
	channel = payload.get('channel') or 'Mialinhcute'
	out = os.path.join(ROOT, 'output', 'api_gen' + str(int(tnttm.time())) + '.mp4')
	item = {'topic': prompt[:120], 'hook': prompt[:100], 'body': prompt, 'search_query': prompt}
	style = {'engine': engine, 'ai_wait': 300, 'ai_overlay': False, 'auto_cdp': engine in ('flow', 'vids', 'auto')}
	t0 = tnttm.time()
	try:
		from modules.render import video as _vmod
		path = _vmod.render(item, out, style)
		elapsed = round(tnttm.time() - t0, 2)
		tnt_engine = {'provider': engine, 'model': engine, 'is_free': True, 'elapsed_sec': elapsed, 'channel': channel, 'generated_by': 'TNT Media OS'}
		return {'ok': True, 'video_path': path, 'elapsed_sec': elapsed, 'tnt_engine': tnt_engine}
	except Exception as e:
		import traceback
		return JSONResponse({'ok': False, 'error': str(e)[:300], 'trace': traceback.format_exc()[-800:]}, status_code=500)


@app.get('/api/video/engine/{name}/health')
def video_engine_health(name: str):
	res = {'engine': name}
	if name == 'luma':
		try:
			from modules.video.http_engine import HTTPVideoEngine
			e = HTTPVideoEngine('luma', poll_interval=2, max_wait=10)
			res['available'] = e.available
		except Exception as ex:
			res['error'] = str(ex)[:200]
	elif name == 'pexels':
		try:
			from modules.render import pexels_fetch
			res['available'] = True
		except Exception as ex:
			res['error'] = str(ex)[:200]
	elif name == 'ffmpeg':
		from ops import ffmpeg_render
		res['available'] = True
	else:
		res['note'] = 'no probe for ' + name
	return res


@app.get('/api/quote/list')
def quote_list(channel: str = None):
	try:
		from modules.render import quote_engine as qe
		lib = qe.load_library()
		out = {}
		for ch in lib.get('channels', {}):
			if channel and ch != channel:
				continue
			cats = lib['channels'][ch].get('categories', {})
			out[ch] = {k: len(v) for k, v in cats.items()}
		return {'ok': True, 'channels': out}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:200]}, status_code=500)


@app.post('/api/quote/generate')
def quote_generate(payload: dict):
	import time as _tq
	channel = payload.get('channel') or 'Mialinhcute'
	category = payload.get('category')
	engine = payload.get('engine')
	try:
		from modules.render import quote_engine as qe
		ts = str(int(_tq.time()))
		out = os.path.join(ROOT, 'output', 'quote_' + channel + '_' + ts + '.mp4')
		style = {'voice': payload.get('voice') or 'female_north'}
		style['voice_preset'] = payload.get('preset') or 'cheerful'
		use_v2 = payload.get('v2', True)
		if use_v2:
			r = qe.make_quote_v2(channel, out, category=category, style=style, engine=(engine or 'auto'))
		else:
			r = qe.make_quote(channel, out, category=category, style=style, engine=(engine or 'auto'))
		return {'ok': r.get('ok'), 'path': r.get('path'), 'final': r.get('final'), 'quote': r.get('quote'), 'error': r.get('error'), 'engine': r.get('engine'), 'score': r.get('score'), 'passes': r.get('passes'), 'vn_quote': r.get('vn_quote'), 'reasons': r.get('reasons'), 'steps': r.get('steps')}
	except Exception as e:
		import traceback
		return JSONResponse({'ok': False, 'error': str(e)[:300], 'trace': traceback.format_exc()[-500:]}, status_code=500)

@app.post('/api/viral/search')
def viral_search(payload: dict = None):
	try:
		from ops import viral_research as vr
		p = payload or {}
		q = p.get('query') or ''
		if not q:
			return {'ok': False, 'error': 'missing query'}
		r = vr.run_search(q, max_results=int(p.get('max_results', 15)), platform=p.get('platform', 'youtube'))
		if r.get('ok'):
			r['saved'] = vr.save(r, name='search')
		return r
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}


@app.post('/api/viral/youtube')
def viral_youtube(payload: dict = None):
	try:
		from ops import viral_research as vr
		p = payload or {}
		r = vr.run_youtube(region=p.get('region', 'VN'), max_results=int(p.get('max_results', 30)))
		if r.get('ok'):
			r['saved'] = vr.save(r, name='youtube')
		return r
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}


@app.post('/api/viral/hashtag')
def viral_hashtag(payload: dict = None):
	try:
		from ops import viral_research as vr
		p = payload or {}
		platform = p.get('platform') or ''
		tag = p.get('tag') or ''
		if not platform or not tag:
			return {'ok': False, 'error': 'missing platform or tag'}
		r = vr.run_hashtag(platform, tag, max_results=int(p.get('max_results', 15)))
		if r.get('ok'):
			r['saved'] = vr.save(r, name='hashtag')
		return r
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}


@app.get('/api/viral/latest')
def viral_latest(n: int = 3):
	try:
		from ops import viral_research as vr
		return {'ok': True, 'items': vr.latest(n)}
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}

def main():
	import uvicorn
	uvicorn.run(app, host='127.0.0.1', port=7777)


if __name__ == '__main__':
	main()
