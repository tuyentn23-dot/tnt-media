# -- coding: utf-8 --
# pipeline/runner.py - Orchestrator chinh (HARD, cam sua)
import os, sys, json, time, argparse
os.environ.setdefault('PYTHONUTF8', '1')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
try:
	from ops import no_window # noqa
except Exception:
	pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state, job as jobmod
try:
	from pipeline import notify, quota
except Exception:
	notify = None; quota = None


def log(msg):
	print('[runner] ', msg, flush=True)


HEARTBEAT = {'stop': None, 'thread': None}


def _start_heartbeat(job_id, interval=30):
	import threading
	stop = threading.Event()
	def _beat():
		while not stop.wait(interval):
			try:
				c = state.init()
				c.execute('UPDATE jobs SET updated_at=? WHERE id=?', (state.now(), job_id))
				c.commit()
			except Exception:
				pass
	t = threading.Thread(target=_beat, daemon=True)
	t.start()
	HEARTBEAT['stop'] = stop
	HEARTBEAT['thread'] = t


def _stop_heartbeat():
	stop = HEARTBEAT.get('stop')
	if stop:
		stop.set()
	HEARTBEAT['stop'] = None
	HEARTBEAT['thread'] = None


def run_job(job, dry_run=False, item_id=None):
	try:
		from pipeline import recovery as _rec
		_rec.recover_stale_jobs()
	except Exception:
		pass
	log('start job: ' + job.job_id + ' channel=' + job.channel_id)
	_start_heartbeat(job.job_id, 30)
	errs = job.validate()
	if errs:
		log('validate FAIL: ' + str(errs))
		return {'ok': False, 'error': errs}
	c = state.init()
	c.execute('INSERT OR REPLACE INTO jobs (id, channel_id, topic, kind, length_override, voice_override, voice_preset, music_mood, count, require_approval, run_at, repeat, status, priority, created_by, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
		(job.job_id, job.channel_id, job.topic, job.kind, job.length_override, job.voice_override, job.voice_preset, job.music_mood, job.count, int(job.require_approval), job.run_at, job.repeat, 'running', job.priority, job.created_by, state.now(), state.now()))
	c.commit()
	if dry_run:
		log('DRY-RUN: bo qua render/publish')
		c.execute('UPDATE jobs SET status=? WHERE id=?', ('done', job.job_id))
		c.commit()
		return {'ok': True, 'mode': 'dry-run', 'job_id': job.job_id}
	try:
		from ops import channel_loader as ch
		from ops import content_freshness as cf
		from pipeline import modules_loader as ml
		MODS = ml.discover()
		def _call(modname, fnname, *args, **kw):
			m = MODS.get(modname)
			if not m or not m['valid']:
				return None
			mod = ml.load_module(m['path'], modname)
			fn = getattr(mod, fnname, None)
			if fn: return fn(*args, **kw)
			return None
	except Exception as e:
		log('import ops FAIL: ' + str(e)[:120])
		c.execute('UPDATE jobs SET status=?, error=? WHERE id=?', ('failed', str(e)[:200], job.job_id))
		c.commit()
		return {'ok': False, 'error': str(e)}
	cfg = ch.load(job.channel_id)
	kinds = [job.kind] if job.kind else cfg.get('content', {}).get('kinds', [])
	if not kinds:
		kinds = ['default']
	cf.set_channel(job.channel_id)
	rendered = []
	errors = []
	try:
		for kind in kinds:
			items = ch.load_content(job.channel_id, kind)
			fresh = [it for it in items if not cf.is_published(cf.signature(it, kind))]
			if not fresh:
				# Fallback: sinh noi dung moi khi het sach (tranh job fail "khong render duoc")
				try:
					from ops import ai_content as _ac
					_seed = (job.topic or '').strip() or None
					_gen = _ac.generate(job.channel_id, kind, limit=3, seed_topic=_seed)
					_fresh2 = [it for it in (_gen or []) if not cf.is_published(cf.signature(it, kind))]
					if _fresh2:
						fresh = _fresh2
						log('regenerated fresh for kind=' + kind + ' n=' + str(len(fresh)))
				except Exception as _ge:
					log('regen err: ' + str(_ge)[:120])
				if not fresh:
					log('no fresh content for kind=' + kind)
					continue
			if item_id:
						items_all = ch.load_content(job.channel_id, kind)
						matches = [x for x in items_all if x.get('id') == item_id]
						if matches:
									item = matches[0]
						else:
									item = fresh[0]
			else:
						item = fresh[0]
			out = os.path.abspath(os.path.join(ROOT, 'output', 'ch' + job.channel_id + '' + item['id'] + '' + time.strftime('%Y%m%d_%H%M%S') + '.mp4'))
			os.makedirs(os.path.dirname(out), exist_ok=True)
			style = dict(cfg.get('style', {}) or {})
			# Ap modules user chon tu UI (neu co)
			try:
				mods = getattr(job, 'modules', None) or {}
				if isinstance(mods, str):
					import json as _jj
					mods = _jj.loads(mods)
				# Caption + music_only
				_opts = (mods or {}).get('_opts', {}) if isinstance(mods, dict) else {}
				style['caption'] = bool(_opts.get('caption', True))
				style['music_only'] = bool(_opts.get('music_only', False))
				# render step -> engine
				rmod = (mods or {}).get('render')
				if rmod:
					if 'flow' in rmod:
						style['engine'] = 'flow'
					elif 'pexels' in rmod:
						style['engine'] = 'pexels'
					elif 'mix' in rmod:
						style['engine'] = 'auto'
					elif 'gacha' in rmod:
						style['engine'] = 'gacha'
					log('module engine override: ' + str(style.get('engine')))
			except Exception as _me:
				log('modules override err: ' + str(_me)[:120])
			if job.voice_override:
				style['voice'] = job.voice_override
			if job.voice_preset:
				style['voice_preset'] = job.voice_preset
				style['preset'] = job.voice_preset
			try:
				r = _call('render.video', 'render', item, out, style=style)
			except Exception as e:
				import traceback
				log('build FAIL: ' + str(e)[:200])
				log(traceback.format_exc()[-1500:])
				errors.append({'kind': kind, 'error': str(e)[:200]})
				continue
			if not os.path.exists(out) or os.path.getsize(out) < 300000:
				log('render output invalid: ' + out)
				errors.append({'kind': kind, 'error': 'output missing or too small'})
				continue
			sig = cf.signature(item, kind)
			c.execute('INSERT OR IGNORE INTO publications (job_id, channel_id, signature, topic, kind, title, file_path, status, created_at) VALUES (?,?,?,?,?,?,?,?,?)', (job.job_id, job.channel_id, sig, item.get('topic'), kind, item.get('hook', '')[:100], out, 'rendered', state.now()))
			c.commit()
			try:
				cf.mark_published(sig, {'job_id': job.job_id, 'kind': kind, 'file': out})
			except Exception as _me:
				log('mark_published err: ' + str(_me)[:80])
			# QUALITY GATE
			try:
				from ops import quality_gate as qg
				qc = qg.check(out)
				if not qc.get('ok'):
					log('QUALITY FAIL: ' + str(qc.get('errors')))
					continue
			except Exception as qe:
				log('quality gate err: ' + str(qe)[:150])
			rendered.append({'path': out, 'kind': kind, 'sig': sig})
			log('rendered: ' + out)
	except Exception as e:
		import traceback
		log('run_job EXC: ' + str(e)[:200])
		log(traceback.format_exc()[-1500:])
		c.execute('UPDATE jobs SET status=?, error=?, updated_at=? WHERE id=?', ('failed', str(e)[:200], state.now(), job.job_id))
		c.commit()
		return {'ok': False, 'error': str(e), 'rendered': len(rendered)}
	if not rendered:
		msg = 'khong render duoc video nao'
		c.execute('UPDATE jobs SET status=?, error=?, updated_at=? WHERE id=?', ('failed', msg, state.now(), job.job_id))
		c.commit()
		return {'ok': False, 'error': msg, 'errors': errors, 'rendered': 0}
								# === PUBLISH STEP (chi khi auto mode, khong can duyet) ===
		published = []
		pmode = str(cfg.get('publish', {}).get('mode', 'approve'))
		auto_pub = (pmode == 'auto') and (job.require_approval is False or job.require_approval == 0)
		if rendered and auto_pub:
			try:
				from ops import os_publish as _op
				for r in rendered:
					row2 = c.execute('SELECT id, title FROM publications WHERE signature=? AND channel_id=?', (r['sig'], job.channel_id)).fetchone()
					if not row2:
						continue
					pid = row2['id']
					ttl = row2['title'] or r['kind']
					try:
						res = _op.publish(r['path'], ttl, '', force=False)
						vid = (res.get('youtube_id') or res.get('id') or res.get('video_id')) if isinstance(res, dict) else None
						c.execute('UPDATE publications SET status=?, youtube_id=?, published_at=? WHERE id=?', ('published', vid, state.now(), pid))
						c.commit()
						published.append(vid)
						log('published: ' + str(vid))
					except Exception as pe:
						log('publish FAIL: ' + str(pe)[:200])
			except Exception as e:
				log('publish module err: ' + str(e)[:200])
	# Do not overwrite a cancelled terminal state (killswitch) with done.
	cur = c.execute('SELECT status FROM jobs WHERE id=?', (job.job_id,)).fetchone()
	cur_status = cur['status'] if cur else None
	if cur_status == 'cancelled':
		return {'ok': False, 'job_id': job.job_id, 'rendered': len(rendered), 'status': cur_status, 'errors': errors}
	status = 'done'
	c.execute('UPDATE jobs SET status=?, updated_at=? WHERE id=? AND status != ?', (status, state.now(), job.job_id, 'cancelled'))
	c.commit()
	return {'ok': True, 'job_id': job.job_id, 'rendered': len(rendered), 'status': status, 'errors': errors}


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('--job-json', type=str, help='JSON cua job')
	ap.add_argument('--channel', type=str)
	ap.add_argument('--topic', type=str, default=None)
	ap.add_argument('--kind', type=str, default=None)
	ap.add_argument('--item-id', type=str, default=None)
	ap.add_argument('--dry-run', action='store_true')
	args = ap.parse_args()
	if args.job_json:
		j = jobmod.Job.from_json(args.job_json)
	elif args.channel:
		j = jobmod.Job(args.channel, topic=args.topic, kind=args.kind, created_by='cli')
	else:
		log('can --job-json hoac --channel')
		return 1
	try:
		r = run_job(j, dry_run=args.dry_run, item_id=getattr(args, 'item_id', None))
	finally:
		_stop_heartbeat()
	try:
		if notify:
			if r.get('ok'):
				notify.job_done(j.job_id, j.channel_id, r.get('rendered', 0))
			else:
				notify.job_failed(j.job_id, j.channel_id, str(r.get('error'))[:200])
	except Exception:
		pass
	print(json.dumps(r, ensure_ascii=False))
	return 0 if r.get('ok') else 1


if __name__ == '__main__':
	sys.exit(main())
