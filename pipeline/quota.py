# -- coding: utf-8 --
# pipeline/quota.py - YouTube quota tracker (10k units/ngay/account)
import os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state

UPLOAD_COST = 1600
DEFAULT_TOTAL = 10000


def today():
	return time.strftime('%Y-%m-%d')


def get(account='default'):
	c = state.connect()
	r = c.execute('SELECT units_used, units_total FROM quota WHERE account=? AND date=?', (account, today())).fetchone()
	if not r:
		return { 'account': account, 'date': today(), 'used': 0, 'total': DEFAULT_TOTAL, 'remaining': DEFAULT_TOTAL }
	return { 'account': account, 'date': today(), 'used': r[0], 'total': r[1], 'remaining': r[1] - r[0] }


def consume(cost=UPLOAD_COST, account='default'):
	c = state.init()
	c.execute('INSERT OR IGNORE INTO quota (account, date, units_used, units_total) VALUES (?,?,?,?)', (account, today(), 0, DEFAULT_TOTAL))
	c.execute('UPDATE quota SET units_used = units_used + ? WHERE account=? AND date=?', (cost, account, today()))
	c.commit()
	q = get(account)
	if q['remaining'] < UPLOAD_COST:
		try:
			from pipeline import notify
			notify.quota_low(account, q['used'], q['total'])
		except Exception:
			pass
	return q


def can_upload(account='default'):
	q = get(account)
	return q['remaining'] >= UPLOAD_COST


def reset(account='default'):
	c = state.init()
	c.execute('DELETE FROM quota WHERE account=? AND date=?', (account, today()))
	c.commit()
	return get(account)


if __name__ == '__main__':
	print('before:', get())
	print('consume:', consume())
	print('can upload:', can_upload())
