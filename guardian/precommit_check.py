# -- coding: utf-8 --
# guardian/precommit_check.py - Chay truoc khi commit
import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

errors = []

# 1. Integrity
try:
	from guardian import integrity as ig
	r = ig.verify()
	if not r.get('ok'):
		if r.get('bad'):
			errors.append('MODIFIED: ' + str(r['bad']))
		if r.get('missing'):
			errors.append('MISSING: ' + str(r['missing']))
except Exception as e:
	errors.append('integrity err: ' + str(e)[:80])

# 2. Manifest vs git
try:
	mr = ig.verify_manifest_git()
	if not mr.get('ok'):
		errors.append('manifest: ' + str(mr.get('err')))
except Exception as e:
	errors.append('manifest err: ' + str(e)[:80])

if errors:
	print('[pre-commit] FAIL')
	for e in errors:
		print(' ' + e)
	sys.exit(1)

print('[pre-commit] Integrity OK')
sys.exit(0)
