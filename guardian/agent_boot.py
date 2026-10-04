# -- coding: utf-8 --
# guardian/agent_boot.py - Bat buoc chay dau moi phien
import os, sys, json, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def hr(t):
	print('=' * 60)
	print(t)
	print('=' * 60)

def check_arch():
	hr('1. KIEN TRUC')
	for d in ['pipeline', 'modules', 'app', 'state', 'guardian']:
		p = os.path.join(ROOT, d)
		mark = '[OK]' if os.path.isdir(p) else '[MISSING]'
		print(' ' + mark + ' ' + d)

def check_db():
	hr('2. DATABASE')
	db = os.path.join(ROOT, 'state', 'pipeline.db')
	if not os.path.exists(db):
		print(' [FAIL] DB khong ton tai')
		return
	c = sqlite3.connect(db)
	print(' DB: ' + db)
	for t in ['channels', 'publications', 'jobs']:
		try:
			n = c.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
			print(' ' + t + ': ' + str(n))
		except Exception as e:
			print(' ' + t + ': ERR')

def check_git():
	hr('3. GIT (5 commit gan nhat)')
	import subprocess
	r = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True, cwd=ROOT)
	for l in r.stdout.splitlines():
		print(' ' + l)
	r2 = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, cwd=ROOT)
	lines = r2.stdout.strip().splitlines()
	if lines:
		print(' Uncommitted: ' + str(len(lines)) + ' files')

def check_critical():
	hr('4. CRITICAL FILES (CAM SUA)')
	crit = os.path.join(ROOT, 'guardian', 'critical.json')
	if not os.path.exists(crit):
		print(' [WARN] critical.json chua co')
		return
	try:
		d = json.load(open(crit, encoding='utf-8'))
		if isinstance(d, list):
			files = d
		elif isinstance(d, dict):
			files = d.get('files', [])
		else:
			files = []
		print(' So file cam sua: ' + str(len(files)))
		missing = [f for f in files if not os.path.exists(os.path.join(ROOT, f))]
		if missing:
			print(' [FAIL] Thieu: ' + str(missing[:3]))
		else:
			print(' [OK] Tat ca critical file ton tai')
	except Exception as e:
		print(' ERR: ' + str(e)[:80])

def check_modules():
	hr('5. MODULES (AGENT LAM VIEC O DAY)')
	md = os.path.join(ROOT, 'modules')
	if not os.path.isdir(md):
		print(' [FAIL]')
		return
	for sub in sorted(os.listdir(md)):
		p = os.path.join(md, sub)
		if not os.path.isdir(p): continue
		py = [f for f in os.listdir(p) if f.endswith('.py') and f != 'init.py']
		print(' ' + sub + ': ' + str(len(py)) + ' modules')

def check_docs():
	hr('6. TAI LIEU PHAI DOC')
	docs = ['BOOTSTRAP.md', 'STATE.md', 'CHANGELOG.md', 'PIPELINE_SPEC.md', 'SYSTEM_OVERVIEW.md']
	for d in docs:
		p = os.path.join(ROOT, d)
		if os.path.exists(p):
			print(' [OK] ' + d + ' (' + str(os.path.getsize(p)) + 'b)')
		else:
			print(' [MISSING] ' + d)

def main():
	hr('AGENT BOOT - TNT MEDIA OS')
	check_arch()
	check_db()
	check_git()
	check_critical()
	check_modules()
	check_docs()
	hr('SAN SANG LAM VIEC')
	print('BUOC TIEP: python guardian/guard.py before')

if __name__ == '__main__':
	main()