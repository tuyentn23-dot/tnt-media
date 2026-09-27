# -- coding: utf-8 --
# pipeline/runner.py - Orchestrator chinh (HARD, cam sua)
import os, sys, json, time, argparse
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


def run_job(job, dry_run=False, item_id=None):
	try:
		from pipeline import recovery as _rec
		_rec.recover_stale_jobs()
	except Exception:
		pass
	log('start job: ' + job.job_id + ' channel=' + job.channel_id)
	errs = job.validate()
	if errs:
		log('validate FAIL: ' + str(errs))
		return {'ok': False, 'error': errs}
	c = state.init()
	c.execute('INSERT OR REPLACE INTO jobs (id, channel_id, topic, kind, length_override, voice_override, music_mood, count, require_approval, run_at, repeat, status, priority, created_by, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
		(job.job_id, job.channel_id, job.topic, job.kind, job.length_override, job.voice_override, job.music_mood, job.count, int(job.require_approval), job.run_at, job.repeat, 'running', job.priority, job.created_by, state.now(), state.now()))
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
			style = cfg.get('style', {})
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
	status = 'done'
	c.execute('UPDATE jobs SET status=?, updated_at=? WHERE id=?', (status, state.now(), job.job_id))
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
	r = run_job(j, dry_run=args.dry_run, item_id=getattr(args, 'item_id', None))
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
