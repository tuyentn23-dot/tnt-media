# -- coding: utf-8 --
# app/tray.py - Tray app + auto-spawn server + Edge app window (P0 upgraded)
import os, sys, time, subprocess, socket, shutil, json, threading
import webbrowser
try:
	from ops import _no_window # noqa
except Exception:
	pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
HOST = '127.0.0.1'
PORT = 7777
URL = 'http://' + HOST + ':' + str(PORT)
APP_URL = URL + '/ui/index.html'
PROC = [None]
WIN = [None]
SCHED_STOP = threading.Event()
LOCK_FILE = os.path.join(ROOT, 'state', 'tray.lock')


def acquire_single_instance():
	try:
		os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
		fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR)
	except Exception:
		return None
	try:
		import msvcrt
		msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
	except Exception:
		return None
	return fd


def port_open(timeout=1.0):
	s = socket.socket()
	s.settimeout(timeout)
	try:
		s.connect((HOST, PORT))
		return True
	except Exception:
		return False
	finally:
		s.close()


def health_ok():
	try:
		import urllib.request
		r = urllib.request.urlopen(URL + '/api/health', timeout=2)
		if r.status != 200:
			return False
		d = json.loads(r.read().decode('utf-8'))
		return d.get('ok') is True
	except Exception:
		return False


def spawn_server():
	if PROC[0] and PROC[0].poll() is None:
		return True
	if health_ok():
		return True
	if port_open() and not health_ok():
		try:
			print('[tray] port ' + str(PORT) + ' bi chiem boi process khac (khong phai TNT Media)')
		except Exception:
			pass
		return False
	cmd = [sys.executable, os.path.join(ROOT, 'app', 'server.py')]
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	logdir = os.path.join(ROOT, 'logs')
	os.makedirs(logdir, exist_ok=True)
	lf = open(os.path.join(logdir, 'server_tray.log'), 'a', encoding='utf-8')
	try:
		PROC[0] = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)
	except Exception:
		PROC[0] = subprocess.Popen(cmd, cwd=ROOT)
	for i in range(30):
		time.sleep(0.5)
		if health_ok():
			return True
	return False


def find_browser():
	cands = [
		os.path.join(os.environ.get('PROGRAMFILES', ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
		os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
		os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
		os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
	]
	for p in cands:
		if p and os.path.exists(p):
			return p
	for nm in ('msedge', 'chrome'):
		p = shutil.which(nm)
		if p:
			return p
	return None


def open_window():
	spawn_server()
	b = find_browser()
	if not b:
		webbrowser.open(APP_URL)
		return
	if WIN[0] and WIN[0].poll() is None:
		return
	args = [b, '--app=' + APP_URL, '--window-size=1100,760', '--window-position=80,60',
		'--user-data-dir=' + os.path.join(ROOT, 'state', 'browser_profile'),
		'--no-first-run', '--no-default-browser-check']
	WIN[0] = subprocess.Popen(args)


def status_text():
	from pipeline import state
	try:
		c = state.connect()
		pubs = c.execute('SELECT COUNT() FROM publications').fetchone()[0]
		jobs = c.execute('SELECT COUNT() FROM jobs').fetchone()[0]
		pend = c.execute("SELECT COUNT(*) FROM publications WHERE status='rendered'").fetchone()[0]
		srv = 'UP' if health_ok() else ('PORT' if port_open() else 'DOWN')
		return 'pubs=' + str(pubs) + ' jobs=' + str(jobs) + ' pending=' + str(pend) + ' server=' + srv
	except Exception as e:
		return 'ERR: ' + str(e)[:80]


def sched_loop():
	try:
		from pipeline import scheduler
		scheduler.run(interval=60, stop_event=SCHED_STOP)
	except Exception as e:
		try:
			print('[tray] scheduler ERR: ' + str(e)[:120])
		except Exception:
			pass


def main():
	lock = acquire_single_instance()
	if lock is None:
		try:
			print('[tray] da co phien khac dang chay. Mo dashboard.')
		except Exception:
			pass
		open_window()
		return 0
	try:
		import pystray
		from PIL import Image, ImageDraw
	except ImportError:
		try:
			print('Can cai: pip install pystray pillow')
		except Exception:
			pass
		return 1
	try:
		print('[tray] spawning server...')
	except Exception:
		pass
	server_ok = spawn_server()
	try:
		print('[tray] server_ok=' + str(server_ok) + ' status=' + status_text())
	except Exception:
		pass
	th = threading.Thread(target=sched_loop, daemon=True)
	th.start()

	def on_open(icon=None, item=None):
		open_window()
	def on_status(icon=None, item=None):
		try:
			print('[tray] ' + status_text())
		except Exception:
			pass
	def on_pause(icon=None, item=None):
		try:
			import os as _os
			_flag = _os.path.join(ROOT, 'state', 'paused.flag')
			_os.makedirs(_os.path.dirname(_flag), exist_ok=True)
			open(_flag, 'w').write('1')
			print('[tray] da tam dung scheduler (flag)')
		except Exception as e:
			print('[tray] pause ERR: ' + str(e)[:120])
	def on_resume(icon=None, item=None):
		try:
			import os as _os
			_flag = _os.path.join(ROOT, 'state', 'paused.flag')
			if _os.path.exists(_flag):
				_os.remove(_flag)
			print('[tray] da tiep tuc scheduler (flag removed)')
		except Exception as e:
			print('[tray] resume ERR: ' + str(e)[:120])
	def on_reconnect(icon=None, item=None):
		try:
			ok = health_ok()
			print('[tray] reconnect: server=' + str(ok))
			if not ok:
				spawn_server()
			open_window()
		except Exception as e:
			print('[tray] reconnect ERR: ' + str(e)[:120])
	def on_open_logs(icon=None, item=None):
		try:
			logdir = os.path.join(ROOT, 'logs')
			os.makedirs(logdir, exist_ok=True)
			os.startfile(logdir)
		except Exception as e:
			print('[tray] open logs ERR: ' + str(e)[:120])
	def on_backup_now(icon=None, item=None):
		try:
			from ops import backup_state as _bs
			from pipeline import state as _st
			bk = os.path.join(ROOT, 'state', 'backup')
			dst = _bs.backup_sqlite(_st.DB, bk)
			print('[tray] backup: ' + dst)
		except Exception as e:
			print('[tray] backup ERR: ' + str(e)[:120])
	def on_quit(icon, item):
		try:
			SCHED_STOP.set()
		except Exception:
			pass
		try:
			if PROC[0] and PROC[0].poll() is None:
				PROC[0].terminate()
		except Exception:
			pass
		try:
			if WIN[0] and WIN[0].poll() is None:
				WIN[0].terminate()
		except Exception:
			pass
		icon.stop()

	img = Image.new('RGB', (64, 64), (59, 130, 246))
	d = ImageDraw.Draw(img)
	d.rectangle((8, 8, 56, 56), outline=(255, 255, 255), width=3)
	d.text((20, 25), 'TNT', fill=(255, 255, 255))
	m1 = pystray.MenuItem('Mo TNT Media', on_open, default=True)
	m2 = pystray.MenuItem('Trang thai', on_status)
	m3 = pystray.MenuItem('Tam dung', on_pause)
	m4 = pystray.MenuItem('Tiep tuc', on_resume)
	m5 = pystray.MenuItem('Khoi phuc ket noi', on_reconnect)
	m6 = pystray.MenuItem('Xem log', on_open_logs)
	m6b = pystray.MenuItem('Backup ngay', on_backup_now)
	m7 = pystray.MenuItem('Thoat', on_quit)
	menu = pystray.Menu(m1, m2, pystray.Menu.SEPARATOR, m3, m4, pystray.Menu.SEPARATOR, m5, m6, m6b, pystray.Menu.SEPARATOR, m7)
	icon = pystray.Icon('tnt', img, 'TNT Media', menu)
	icon.run()
	return 0


if __name__ == '__main__':
	sys.exit(main())
