# -- coding: utf-8 --
"""scheduler_cc - YC1: dang deu dan theo cron moi kenh."""
import os, sys, json, time, sqlite3
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
if not os.path.isdir(os.path.join(ROOT, 'ops')):
	ROOT = os.getcwd()
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, 'system', 'state.db')
LOG = os.path.join(ROOT, 'logs', 'scheduler_cc.log')

def log(m):
	try:
		os.makedirs(os.path.dirname(LOG), exist_ok=True)
		with open(LOG, 'a', encoding='utf-8') as f:
			f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + str(m) + chr(10))
	except Exception:
		pass

def parse_cron(expr):
	p = (expr or '').split()
	return p if len(p) == 5 else None

def field_match(field, val, lo, hi):
	for part in field.split(','):
		step = 1
		if '/' in part:
			part, s = part.split('/', 1)
			step = int(s)
		if part == '*':
			rng = range(lo, hi + 1, step)
		elif '-' in part:
			x, y = part.split('-', 1)
			rng = range(int(x), int(y) + 1, step)
		else:
			rng = range(int(part), int(part) + 1)
		if val in rng:
			return True
	return False

def due(expr, now):
	p = parse_cron(expr)
	if not p:
		return False
	mn, hr, dom, mo, dow = p
	ok = field_match(mn, now.minute, 0, 59)
	ok = ok and field_match(hr, now.hour, 0, 23)
	ok = ok and field_match(dom, now.day, 1, 31)
	ok = ok and field_match(mo, now.month, 1, 12)
	ok = ok and field_match(dow, (now.weekday() + 1) % 7, 0, 6)
	return ok

def channels():
	con = sqlite3.connect(DB)
	rows = list(con.execute("SELECT name, scheduleCron, active FROM channels WHERE active=1"))
	con.close()
	return rows

def tick(now=None):
	now = now or datetime.now()
	fired = []
	for name, cron, active in channels():
		if due(cron, now):
			fired.append(name)
	return fired

def run_channel(name):
	from ops import channel_producer as CP
	log('RUN ' + name)
	rows = CP.run_many(name, limit=1, live=True)
	log(name + ' -> ' + json.dumps(rows, ensure_ascii=True))
	return rows

def main():
	log('scheduler_cc start')
	done = set()
	while True:
		now = datetime.now()
		key = now.strftime('%Y-%m-%d %H:%M')
		for name in tick(now):
			k = key + '|' + name
			if k in done:
				continue
			done.add(k)
			try:
				run_channel(name)
			except Exception as e:
				log(name + ' ERROR ' + str(e))
		time.sleep(30)

if os.path.basename(sys.argv[0]).startswith('scheduler_cc'):
	main()
