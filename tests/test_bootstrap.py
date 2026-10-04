# -- coding: utf-8 --
# Test kiem tra 4 yeu cau: nho, khong sai, khong pha, 100%
import os, sys, json, subprocess
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestArchitecture:
	def test_pipeline_exists(self):
		assert os.path.isdir(os.path.join(ROOT, 'pipeline'))

	def test_modules_exists(self):
		assert os.path.isdir(os.path.join(ROOT, 'modules'))

	def test_app_exists(self):
		assert os.path.isdir(os.path.join(ROOT, 'app'))

	def test_guardian_exists(self):
		assert os.path.isdir(os.path.join(ROOT, 'guardian'))


class TestDocumentation:
	'''Yeu cau 1: Nho moi lan'''

	def test_bootstrap_md(self):
		p = os.path.join(ROOT, 'BOOTSTRAP.md')
		assert os.path.exists(p), 'BOOTSTRAP.md phai ton tai'
		assert os.path.getsize(p) > 1000, 'BOOTSTRAP.md phai co noi dung'

	def test_state_md(self):
		assert os.path.exists(os.path.join(ROOT, 'STATE.md'))

	def test_changelog(self):
		assert os.path.exists(os.path.join(ROOT, 'CHANGELOG.md'))

	def test_system_overview(self):
		assert os.path.exists(os.path.join(ROOT, 'SYSTEM_OVERVIEW.md'))

	def test_pipeline_spec(self):
		assert os.path.exists(os.path.join(ROOT, 'PIPELINE_SPEC.md'))


class TestCriticalFiles:
	'''Yeu cau 3: Khong pha cai da lam'''

	def test_critical_json_valid(self):
		p = os.path.join(ROOT, 'guardian', 'critical.json')
		assert os.path.exists(p)
		d = json.load(open(p, encoding='utf-8'))
		assert isinstance(d, dict)
		assert 'pipeline_hard' in d
		assert 'bootstrap' in d

	def test_all_critical_files_exist(self):
		p = os.path.join(ROOT, 'guardian', 'critical.json')
		d = json.load(open(p, encoding='utf-8'))
		missing = []
		for group, files in d.items():
			for f in files:
				fp = os.path.join(ROOT, f)
				if not os.path.exists(fp):
					missing.append(f)
		assert not missing, 'Critical files thieu: ' + str(missing)

	def test_pipeline_db_exists(self):
		p = os.path.join(ROOT, 'state', 'pipeline.db')
		assert os.path.exists(p), 'DB la nguon su that'


class TestModulesLoadable:
	'''Yeu cau 2: Khong sai - tat ca module phai load duoc'''

	def test_agent_boot(self):
		p = os.path.join(ROOT, 'guardian', 'agent_boot.py')
		assert os.path.exists(p)
		import ast
		ast.parse(open(p, encoding='utf-8').read())

	def test_modules_parse(self):
		md = os.path.join(ROOT, 'modules')
		bad = []
		for sub in os.listdir(md):
			p = os.path.join(md, sub)
			if not os.path.isdir(p):
				continue
			for f in os.listdir(p):
				if not f.endswith('.py'):
					continue
				fp = os.path.join(p, f)
				try:
					import ast
					ast.parse(open(fp, encoding='utf-8').read())
				except SyntaxError as e:
					bad.append(f + ': ' + str(e)[:60])
		assert not bad, 'Modules loi syntax: ' + str(bad)

	def test_pipeline_parse(self):
		pd = os.path.join(ROOT, 'pipeline')
		bad = []
		for f in os.listdir(pd):
			if not f.endswith('.py'):
				continue
			fp = os.path.join(pd, f)
			try:
				import ast
				ast.parse(open(fp, encoding='utf-8').read())
			except SyntaxError as e:
				bad.append(f + ': ' + str(e)[:60])
		assert not bad, 'Pipeline loi syntax: ' + str(bad)


class TestSelfcheck:
	'''Yeu cau 4: 100% dam bao'''

	def test_selfcheck_runs(self):
		r = subprocess.run(
			[sys.executable, '-m', 'pipeline.selfcheck'],
			capture_output=True, text=True, cwd=ROOT, timeout=30
		)
		assert r.returncode == 0, 'Selfcheck phai pass: ' + r.stdout[-200:]
		out = r.stdout
		# Check khong co [FAIL]
		fails = [l for l in out.splitlines() if '[FAIL]' in l]
		assert not fails, 'Selfcheck co FAIL: ' + str(fails)

	def test_guardian_verify(self):
		r = subprocess.run(
			[sys.executable, 'guardian/guard.py', 'verify'],
			capture_output=True, text=True, cwd=ROOT, timeout=30
		)
		assert 'MISSING: none' in r.stdout, 'Guardian verify fail: ' + r.stdout[:200]
