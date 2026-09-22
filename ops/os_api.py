# -- coding: utf-8 --
"""os_api - YC7: quota per channel + channels full cho dashboard."""
import os, sys, json, sqlite3
from datetime import datetime, timedelta, timezone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
if not os.path.isdir(os.path.join(ROOT, 'ops')):
	ROOT = os.getcwd()
DB = os.path.join(ROOT, 'system', 'state.db')
DAILY_QUOTA_DEFAULT = 3

def _channel_cfg(name):
	p = os.path.join(ROOT, 'channels', name + '.json')
	try:
		return json.load(open(p, encoding='utf-8'))
	except Exception:
		return {}

def quotas():
	con = sqlite3.connect(DB)
	con.row_factory = sqlite3.Row
	chans = [dict(r) for r in con.execute('SELECT id, name, active, scheduleCron, maxSeconds FROM channels')]
	since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
	out = []
	for c in chans:
		cfg = _channel_cfg(c['name'])
		quota = int(cfg.get('dailyQuota', DAILY_QUOTA_DEFAULT))
		used = con.execute('SELECT COUNT() FROM videos WHERE channelId=? AND createdAt>=?', (c['id'], since)).fetchone()[0]
		vid = con.execute('SELECT COUNT() FROM videos WHERE channelId=?', (c['id'],)).fetchone()[0]
		out.append(dict(id=c['id'], name=c['name'], active=c['active'], cron=c['scheduleCron'], maxSeconds=c['maxSeconds'], topics=cfg.get('topics', []), tokenPath=cfg.get('tokenPath'), voice=cfg.get('voicePreset'), quota=quota, used24h=used, remaining=max(0, quota - used), videos=vid))
	con.close()
	return dict(updatedAt=datetime.now().isoformat(timespec='seconds'), channels=out)

def add_routes(app):
	from fastapi.responses import JSONResponse
	@app.get('/api/quotas')
	def api_quotas():
		return JSONResponse(quotas())
	@app.get('/api/os/state')
	def api_os_state():
		return JSONResponse(quotas())
	return app
