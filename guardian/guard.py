# -- coding: utf-8 --
# guardian/guard.py - Wrapper before/verify
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def before():
	try:
		from guardian import snapshot as sn
		p = sn.snapshot()
		print('SNAPSHOT OK: ' + str(p))
	except Exception as e:
		print('SNAPSHOT FAIL: ' + str(e))
		sys.exit(1)

def verify():
	errors = []
	try:
		from guardian import snapshot as sn
		m = sn.verify()
		if m:
			errors.append('missing: ' + str(m))
	except Exception as e:
		errors.append('snapshot err: ' + str(e))
	try:
		from guardian import integrity as ig
		r = ig.verify()
		if not r.get('ok'):
			if r.get('bad'):
				errors.append('modified: ' + str(r['bad']))
			if r.get('missing'):
				errors.append('missing-critical: ' + str(r['missing']))
	except Exception as e:
		errors.append('integrity err: ' + str(e))
	if errors:
		print('GUARD FAIL:')
		for e in errors:
			print(' ' + str(e))
		sys.exit(1)
	print('MISSING: none')
	print('INTEGRITY: OK')
	sys.exit(0)

def main():
	import sys
	if len(sys.argv) < 2:
		print('Usage: guard.py before|verify')
		sys.exit(1)
	cmd = sys.argv[1]
	if cmd == 'before':
		before()
	elif cmd == 'verify':
		verify()
	else:
		print('Unknown: ' + cmd)
		sys.exit(1)

if __name__ == '__main__':
	main()