# -- coding: utf-8 --
import os, sys, time, tempfile, shutil, subprocess, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from playwright.sync_api import sync_playwright
PORT = '7787'
def setup_isolated():
	d = tempfile.mkdtemp()
	db = os.path.join(d, 'pipeline.db')
	src = os.path.join(ROOT, 'state', 'pipeline.db')
	if os.path.exists(src):
		shutil.copy(src, db)
	cfg = os.path.join(d, 'ui_config.json')
	json.dump({"publish_mode": "approve"}, open(cfg, 'w'))
	out = os.path.join(d, 'output')
	os.makedirs(out, exist_ok=True)
	vid = os.path.join(out, 'fixture.mp4')
	open(vid, 'wb').write(b'')
	return d, db, vid
def main():
	d, db, vid = setup_isolated()
	env = dict(os.environ)
	env['TNT_TEST_DB'] = db
	env['TNT_TEST_CONFIG'] = os.path.join(d, 'ui_config.json')
	env['TNT_TEST_OUTPUT'] = os.path.dirname(vid)
	proc = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app.server:app', '--port', PORT], cwd=ROOT, env=env)
	time.sleep(6)
	errs = []
	with sync_playwright() as pw:
		b = pw.chromium.launch()
		pg = b.new_page()
		pg.add_init_script("document.addEventListener('alpine:init',function(){var o=Alpine.evaluate;Alpine.evaluate=function(el,e){try{return o.call(Alpine,el,e)}catch(err){console.log('ALPINE_FAIL:'+e+'::'+err.message);throw err}}})")
		pg.add_init_script("window.addEventListener('error', e => console.error('ERRSTACK', e.error && e.error.stack, e.message))")
		pg.on('pageerror', lambda e: errs.append(str(e)+chr(124)+(getattr(e,chr(39)+chr(115)+chr(116)+chr(97)+chr(99)+chr(107)+chr(39), chr(39)+chr(39)) or chr(39)+chr(39))))
		pg.goto('http://127.0.0.1:' + PORT + '/ui/index.html')
		pg.wait_for_timeout(2500)
		print('TITLE', pg.title())
		print('JS_ERRORS', errs)
		print('TABS', pg.locator('.tab').count())
		print('TAB0', pg.locator('.tab').first.inner_text() if pg.locator('.tab').count() else 'none')
		b.close()
	proc.terminate()
	print('=== UI RESULT ===')
	return 0
if __name__ == '__main__':
	sys.exit(main())
