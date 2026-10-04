# -- coding: utf-8 --
# guardian/session_end.py - Ket thuc phien lam viec
import os, sys, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def hr(t):
	print('=' * 60)
	print(t)
	print('=' * 60)

def run(cmd):
	r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, shell=True)
	return r.returncode, r.stdout, r.stderr

def check_all():
	hr('KIEM TRA CUOI PHIEN')
	checks = [
		('guardian verify', 'python guardian/guard.py verify'),
		('selfcheck', 'python -m pipeline.selfcheck'),
		('tests', 'python -m pytest tests/test_bootstrap.py -q'),
	]
	all_ok = True
	for name, cmd in checks:
		rc, out, err = run(cmd)
		ok = rc == 0
		if not ok:
			all_ok = False
		mark = '[OK]' if ok else '[FAIL]'
		print(' ' + mark + ' ' + name)
	return all_ok

def print_history():
	hr('LICH SU GAN NHAT')
	rc, out, err = run('git log --oneline -5')
	for l in out.splitlines():
		print(' ' + l)

def main():
	hr('SESSION END - TNT MEDIA OS')
	ok = check_all()
	print_history()
	hr('KET THUC')
	if ok:
		print(' [OK] Phien hoan tat thanh cong')
	else:
		print(' [FAIL] Co check chua pass - KHONG ket thuc')
		sys.exit(1)

if __name__ == '__main__':
	main()