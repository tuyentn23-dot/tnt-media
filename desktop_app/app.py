# -- coding: utf-8 --
# desktop_app/app.py - Main window.
# Architecture (4 primary tabs, Apple-style single-purpose surfaces):
#   1. Studio   - daily work: create (Pipeline/Weekly) + queue in one screen
#   2. Library  - past work: publications / jobs / modules
#   3. Channels - channel configuration
#   4. Settings - system configuration
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
	QPushButton, QStackedWidget, QButtonGroup, QFrame, QStatusBar
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
import i18n, theme, tray, prefs, icons


class Toast(QLabel):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setObjectName('Toast')
		self.setVisible(False)
		self.setAlignment(Qt.AlignCenter)

	def pop(self, text, ms=3000):
		self.setText(text)
		self.adjustSize()
		self.setVisible(True)
		self.raise_()
		QTimer.singleShot(ms, lambda: self.setVisible(False))


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setMinimumSize(1180, 720)
		self.resize(1520, 900)
		self._prefs = prefs.load()
		self._theme = self._prefs.get('theme', 'light')
		self._build()
		self._apply_theme()

	def _apply_theme(self):
		self.setStyleSheet(theme.stylesheet(self._theme))

	def set_theme(self, name):
		self._theme = name
		self._apply_theme()
		try:
			self._prefs['theme'] = name
			prefs.save(self._prefs)
		except Exception:
			pass

	def _build(self):
		self.setWindowTitle(i18n.t('app.name'))
		icon_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
		if os.path.exists(icon_p):
			self.setWindowIcon(QIcon(icon_p))
		central = QWidget()
		self.setCentralWidget(central)
		lay = QHBoxLayout(central)
		lay.setContentsMargins(0, 0, 0, 0)
		lay.setSpacing(0)

		side = QFrame()
		side.setObjectName('Sidebar')
		side.setFixedWidth(240)
		sv = QVBoxLayout(side)
		sv.setContentsMargins(16, 20, 16, 14)
		sv.setSpacing(2)

		brand = QLabel("TNT")
		brand.setStyleSheet('font-size:24px;font-weight:800;color:#0A84FF;padding:6px 10px')
		sv.addWidget(brand)
		sub = QLabel(i18n.t('app.sub'))
		sub.setStyleSheet('font-size:11px;color:#8E8E93;padding:0 10px 10px 10px')
		sv.addWidget(sub)
		sep = QFrame()
		sep.setFrameShape(QFrame.HLine)
		sep.setStyleSheet('color:#D9D9DE;margin:4px 6px')
		sv.addWidget(sep)

		self.stack = QStackedWidget()
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)

		from views.studio import Studio
		from views.library import Library
		from views.channels import Channels
		from views.settings import Settings

		self.views = []
		self.btn_map = []

		def add(key, factory, icon_key=None):
			try:
				w = factory(self) if factory is Settings else factory()
			except Exception as e:
				w = QLabel('View error: ' + str(e))
				w.setAlignment(Qt.AlignCenter)
			self.views.append(w)
			self.stack.addWidget(w)
			lbl = i18n.t(key)
			ic_name = icon_key or key.replace('nav.', '')
			b = QPushButton(lbl)
			b.setIcon(icons.icon(ic_name, 18, '#3A3A3C'))
			b.setIconSize(QSize(18, 18))
			b.setStyleSheet('text-align:left;padding-left:12px')
			b.setCheckable(True)
			b.setCursor(Qt.PointingHandCursor)
			b.setMinimumHeight(38)
			idx = len(self.views) - 1
			b.clicked.connect(lambda _=False, i=idx: self.go(i))
			self.group.addButton(b, idx)
			sv.addWidget(b)
			self.btn_map.append(b)

		add('nav.studio', Studio)
		add('nav.library', Library)
		add('nav.channels', Channels)
		add('nav.settings', Settings)

		sv.addStretch()
		lang_btn = QPushButton("VI | EN")
		lang_btn.setToolTip('Doi ngon ngu (VI/EN)')
		lang_btn.setCursor(Qt.PointingHandCursor)
		lang_btn.clicked.connect(self.toggle_lang)
		sv.addWidget(lang_btn)
		ver = QLabel('v4.0')
		ver.setStyleSheet('font-size:10px;color:#8E8E93;padding:6px 10px')
		sv.addWidget(ver)

		lay.addWidget(side)
		lay.addWidget(self.stack, 1)

		try:
			self.go(int(self._prefs.get('last_tab', 0)))
		except Exception:
			self.go(0)

		sb = QStatusBar()
		self.setStatusBar(sb)
		self.status_lbl = QLabel('San sang')
		self.status_lbl.setStyleSheet('padding:0 8px')
		sb.addWidget(self.status_lbl)
		self.jobs_lbl = QLabel('')
		sb.addPermanentWidget(self.jobs_lbl)

		self.toast = Toast(central)
		self._status_timer = QTimer(self)
		self._status_timer.timeout.connect(self._refresh_status)
		self._status_timer.start(10000)
		self._refresh_status()
		self._setup_shortcuts()

	def _setup_shortcuts(self):
		sc = QShortcut(QKeySequence('Ctrl+R'), self)
		sc.activated.connect(self._refresh_current)
		sc = QShortcut(QKeySequence('F5'), self)
		sc.activated.connect(self._refresh_status)
		sc = QShortcut(QKeySequence('Ctrl+F'), self)
		sc.activated.connect(self._focus_search)
		for i in range(4):
			sc = QShortcut(QKeySequence('Ctrl+' + str(i + 1)), self)
			sc.activated.connect(lambda ix=i: self.go(ix))

	def _refresh_current(self):
		try:
			w = self.stack.currentWidget()
			if hasattr(w, 'refresh'):
				w.refresh()
			self.pop('Da lam moi', 1500)
		except Exception as e:
			self.pop('Loi: ' + str(e)[:80])

	def _focus_search(self):
		try:
			w = self.stack.currentWidget()
			if hasattr(w, 'search'):
				w.search.setFocus()
				w.search.selectAll()
		except Exception:
			pass

	def pop(self, msg, ms=3000):
		self.toast.pop(msg, ms)
		self.toast.move(self.width() - self.toast.width() - 30, self.height() - 90)

	def _refresh_status(self):
		try:
			import api
			h = api.health()
			if h.get('ok'):
				pub = h.get('publications', 0)
				jb = h.get('jobs', 0)
				self.status_lbl.setText(chr(9679) + ' Server ON pub=' + str(pub) + ' job=' + str(jb))
				self.status_lbl.setStyleSheet('color:#34C759;font-weight:600;padding:0 8px')
			else:
				self.status_lbl.setText(chr(9679) + ' Server OFF')
				self.status_lbl.setStyleSheet('color:#FF453A;font-weight:600;padding:0 8px')
			se = h.get('scheduler_error') or {}
			alive = se.get('alive')
			stale = se.get('stale')
			if alive and not stale:
				self.jobs_lbl.setText(chr(9200) + ' Scheduler running')
				self.jobs_lbl.setStyleSheet('color:#0A84FF;font-weight:600;padding:0 8px')
			elif alive:
				self.jobs_lbl.setText(chr(9888) + ' Scheduler stale')
				self.jobs_lbl.setStyleSheet('color:#FF9500;font-weight:600;padding:0 8px')
			else:
				self.jobs_lbl.setText(chr(10060) + ' Scheduler off')
				self.jobs_lbl.setStyleSheet('color:#FF453A;font-weight:600;padding:0 8px')
		except Exception as e:
			self.status_lbl.setText(str(e)[:60])

	def go(self, idx):
		if 0 <= idx < len(self.views):
			self.stack.setCurrentIndex(idx)
			self.btn_map[idx].setChecked(True)
			try:
				self._prefs['last_tab'] = int(idx)
				prefs.save(self._prefs)
			except Exception:
				pass

	def toggle_lang(self):
		cur = i18n.get_lang()
		new = 'en' if cur == 'vi' else 'vi'
		i18n.set_lang(new)
		self.rebuild_ui()

	def rebuild_ui(self):
		self._build()
		self._apply_theme()


def _is_up(host='127.0.0.1', port=7777, timeout=0.6):
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(timeout)
	try:
		s.connect((host, port))
		return True
	except Exception:
		return False
	finally:
		s.close()


def _spawn_detached(args, cwd, log_name):
	import subprocess
	os.makedirs(os.path.join(cwd, 'logs'), exist_ok=True)
	lf = open(os.path.join(cwd, 'logs', log_name), 'a', encoding='utf-8')
	flags = 0
	for nm in ('CREATE_NEW_PROCESS_GROUP', 'CREATE_NO_WINDOW'):
		flags = flags | getattr(subprocess, nm, 0)
	try:
		p = subprocess.Popen(args, cwd=cwd, stdout=lf, stderr=subprocess.STDOUT, creationflags=flags, close_fds=True)
		return p.pid
	except Exception:
		return None


def _bootstrap():
	base = _ROOT
	py = os.path.join(base, '.venv', 'Scripts', 'python.exe')
	if not os.path.exists(py):
		py = sys.executable
	if not _is_up(port=7777):
		_spawn_detached([py, os.path.join(base, 'app', 'server.py')], base, 'desktop_server.log')
	if not _sched_ok(base):
		_spawn_detached([py, '-m', 'pipeline.scheduler'], base, 'desktop_scheduler.log')


def _sched_ok(base):
	import json, time
	p = os.path.join(base, 'state', 'scheduler_status.json')
	if not os.path.exists(p):
		return False
	try:
		age = time.time() - os.path.getmtime(p)
		return age < 170
	except Exception:
		return False


def run():
	try:
		_bootstrap()
	except Exception:
		pass
	try:
		import ctypes
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('TNT.Media.Studio.1')
	except Exception:
		pass
	app = QApplication.instance() or QApplication(sys.argv)
	w = MainWindow()
	w.show()
	icon_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
	tray.attach(w, icon_p)
	return app.exec()


if __name__ == '__main__':
	sys.exit(run())
