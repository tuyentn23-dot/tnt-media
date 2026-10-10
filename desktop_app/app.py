# -- coding: utf-8 --
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QButtonGroup, QFrame, QStatusBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
import i18n, theme, tray, prefs


ICONS = {
	'dashboard': "🏠",
	'channels': "📺",
	'pipeline': "🎬",
	'queue': "📥",
	'jobs': "🛠",
	'pubs': "📹",
	'modules': "🧩",
	'settings': "⚙",
}


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
		self.resize(1320, 840)
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
		side.setFixedWidth(230)
		sv = QVBoxLayout(side)
		sv.setContentsMargins(12, 18, 12, 12)
		sv.setSpacing(4)
		brand = QLabel("TNT")
		brand.setStyleSheet('font-size:24px;font-weight:800;color:#0A84FF;padding:6px 10px')
		sv.addWidget(brand)
		sub = QLabel(i18n.t('app.sub'))
		sub.setStyleSheet('font-size:11px;color:#8E8E93;padding:0 10px 10px 10px')
		sv.addWidget(sub)
		sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setStyleSheet('color:#D9D9DE;margin:4px 6px')
		sv.addWidget(sep)
		self.stack = QStackedWidget()
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)
		from views.dashboard import Dashboard
		from views.channels import Channels
		from views.pipeline import Pipeline
		from views.queue import Queue
		from views.tables import Jobs, Pubs, Modules
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
			ic = ICONS.get(icon_key or key.replace('nav.',''), '')
			b = QPushButton(ic + chr(32) + lbl)
			b.setCheckable(True)
			b.setCursor(Qt.PointingHandCursor)
			b.setMinimumHeight(38)
			idx = len(self.views) - 1
			b.clicked.connect(lambda _=False, i=idx: self.go(i))
			self.group.addButton(b, idx)
			sv.addWidget(b)
			self.btn_map.append(b)
		add('nav.dashboard', Dashboard)
		add('nav.channels', Channels)
		add('nav.pipeline', Pipeline)
		add('nav.queue', Queue)
		add('nav.jobs', Jobs)
		add('nav.pubs', Pubs)
		add('nav.modules', Modules)
		add('nav.settings', Settings)
		sv.addStretch()
		lang_btn = QPushButton("VI | EN")
		lang_btn.setCursor(Qt.PointingHandCursor)
		lang_btn.clicked.connect(self.toggle_lang)
		sv.addWidget(lang_btn)
		ver = QLabel('v3.1')
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
		for i in range(8):
			sc = QShortcut(QKeySequence('Ctrl+' + str(i+1)), self)
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


def run():
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
