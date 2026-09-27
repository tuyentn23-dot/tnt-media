# -- coding: utf-8 --
# app/_routes_publish.py - Publish endpoints (P0.3)
# Tach rieng de giam rui ro sua server.py chinh.
import os, sys, json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state
from pipeline import job as jobmod

router = APIRouter()


@router.post('/api/publications/{pub_id}/publish')
def publish_pub(pub_id: int, privacy: str = 'public', force: bool = False):
	c = state.init()
	row = c.execute('SELECT id, channel_id, kind, topic, title, file_path, status, youtube_id FROM publications WHERE id=?', (pub_id,)).fetchone()
	if not row:
		return JSONResponse({'ok': False, 'error': 'publication not found'}, status_code=404)
	if row['youtube_id']:
		return {'ok': True, 'already_published': True, 'youtube_id': row['youtube_id']}
	cur = row['status']
	if cur != 'approved' and not force:
		return JSONResponse({'ok': False, 'error': 'publication chua duoc duyet (status=' + str(cur) + ')', 'status': cur}, status_code=409)
	if not jobmod.valid_transition(jobmod.PUB_TRANSITIONS, cur, 'publishing') and not force:
		return JSONResponse({'ok': False, 'error': 'transition khong hop le: ' + str(cur) + ' -> publishing'}, status_code=409)
	vp = row['file_path']
	if not vp or not os.path.exists(vp):
		return JSONResponse({'ok': False, 'error': 'file khong ton tai: ' + str(vp)}, status_code=400)
	cur2 = c.execute('UPDATE publications SET status=? WHERE id=? AND status=?', ('publishing', pub_id, cur))
	c.commit()
	if cur2.rowcount != 1:
		return JSONResponse({'ok': False, 'error': 'publication da duoc xu ly boi request khac', 'status': 'publishing'}, status_code=409)
	try:
		from ops import os_publish
		os_publish.set_channel(row['channel_id'])
		title = row['title'] or ('TNT Media ' + str(pub_id))
		r = os_publish.publish(vp, title, description='', tags=[], privacy=privacy, topic=row['topic'] or '')
	except Exception as e:
		import traceback
		err = str(e)[:300]
		c.execute('UPDATE publications SET status=? WHERE id=?', ('publish_failed', pub_id))
		c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'publish_failed', str(pub_id), err, state.now()))
		c.commit()
		return JSONResponse({'ok': False, 'error': err, 'trace': traceback.format_exc()[-800:]}, status_code=500)
	if not r or not r.get('ok'):
		err = (r or {}).get('error') or (r or {}).get('reason') or 'publish that bai'
		c.execute('UPDATE publications SET status=? WHERE id=?', ('publish_failed', pub_id))
		c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'publish_failed', str(pub_id), str(err)[:200], state.now()))
		c.commit()
		return JSONResponse({'ok': False, 'error': str(err), 'publish_result': r}, status_code=502)
	yid = r.get('youtube_id')
	if not yid:
		c.execute('UPDATE publications SET status=? WHERE id=?', ('publish_failed', pub_id))
		c.commit()
		return JSONResponse({'ok': False, 'error': 'YouTube khong tra ve id', 'publish_result': r}, status_code=502)
	c.execute('UPDATE publications SET status=?, youtube_id=?, published_at=? WHERE id=?', ('published', yid, state.now(), pub_id))
	c.execute('INSERT INTO audit (session, actor, action, target, reason, ts) VALUES (?,?,?,?,?,?)', ('api', 'ui', 'published', str(pub_id), 'youtube_id=' + str(yid), state.now()))
	c.commit()
	return {'ok': True, 'youtube_id': yid, 'url': r.get('url'), 'score': r.get('score')}


@router.post('/api/publications/{pub_id}/unpublish')
def unpublish_pub(pub_id: int):
	return JSONResponse({'ok': False, 'error': 'chuc nang xoa video YouTube chua duoc bat (yeu cau rieng)'}, status_code=403)
