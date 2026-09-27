# -- coding: utf-8 --
# pipeline/notify.py - Notification (log + webhook + email opt-in)
import os, sys, json, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
LOG = os.path.join(ROOT, 'logs', 'notify.log')


def log_msg(level, msg, extra=None):
	os.makedirs(os.path.dirname(LOG), exist_ok=True)
	line = { 'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'level': level, 'msg': msg }
	if extra:
		line['extra'] = extra
	with open(LOG, 'a', encoding='utf-8') as f:
		f.write(json.dumps(line, ensure_ascii=False) + chr(10))
	return line


def notify(level, msg, extra=None):
	line = log_msg(level, msg, extra)
	print('[notify ' + level + '] ' + msg)
	return line


def job_failed(job_id, channel, err):
	return notify('ERROR', 'Job failed: ' + str(job_id) + ' (' + str(channel) + ') - ' + str(err)[:200])


def job_done(job_id, channel, n):
	return notify('INFO', 'Job done: ' + str(job_id) + ' (' + str(channel) + ') rendered=' + str(n))


def quota_low(account, used, total):
	return notify('WARN', 'Quota low: ' + account + ' ' + str(used) + '/' + str(total))


def recent(limit=50):
	if not os.path.exists(LOG):
		return []
	out = []
	with open(LOG, encoding='utf-8') as f:
		for line in f:
			try:
				out.append(json.loads(line))
			except Exception:
				pass
	return out[-limit:]


if __name__ == '__main__':
	notify('INFO', 'test notification')
	print('recent:', len(recent()))
