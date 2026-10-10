# -- coding: utf-8 --
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QButtonGroup, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import i18n, theme, tray

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setMinimumSize(1180, 720)
		self.resize(1280, 800)
		self._theme = 'light'
		self._build()
		self._apply_theme()

	def _apply_theme(self):
		self.setStyleSheet(theme.stylesheet(self._theme))

	def set_theme(self, name):
		self._theme = name
		self._apply_theme()

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
		side.setFixedWidth(220)
		sv = QVBoxLayout(side)
		sv.setContentsMargins(12, 16, 12, 12)
		sv.setSpacing(4)
		brand = QLabel('TNT')
		brand.setStyleSheet('font-size:22px;font-weight:800;color:#0A84FF;padding:6px 10px')
		sv.addWidget(brand)
		sub = QLabel(i18n.t('app.sub'))
		sub.setStyleSheet('font-size:11px;color:#8E8E93;padding:0 10px 8px 10px')
		sv.addWidget(sub)
		self.stack = QStackedWidget()
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)
		from views.dashboard import Dashboard
		from views.channels import Channels
		from views.pipeline import Pipeline
		from views.tables import Jobs, Pubs, Modules
		from views.queue import Queue
		from views.settings import Settings
		self.views = []
		self.btn_map = []
		def add(key, factory):
			try:
				w = factory(self) if factory is Settings else factory()
			except Exception as e:
				w = QLabel('View error: ' + str(e))
				w.setAlignment(Qt.AlignCenter)
			self.views.append(w)
			self.stack.addWidget(w)
			b = QPushButton(i18n.t(key))
			b.setCheckable(True)
			b.setCursor(Qt.PointingHandCursor)
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
		lang_btn = QPushButton('VI | EN')
		lang_btn.setCursor(Qt.PointingHandCursor)
		lang_btn.clicked.connect(self.toggle_lang)
		sv.addWidget(lang_btn)
		ver = QLabel('v3.0')
		ver.setStyleSheet('font-size:10px;color:#8E8E93;padding:6px 10px')
		sv.addWidget(ver)
		lay.addWidget(side)
		lay.addWidget(self.stack, 1)
		self.go(0)

	def go(self, idx):
		if 0 <= idx < len(self.views):
			self.stack.setCurrentIndex(idx)
			self.btn_map[idx].setChecked(True)

	def toggle_lang(self):
		cur = i18n.get_lang()
		new = 'en' if cur == 'vi' else 'vi'
		i18n.set_lang(new)
		self.rebuild_ui()
	def rebuild_ui(self):
		self._build()
		self._apply_theme()

def run():
	app = QApplication.instance() or QApplication(sys.argv)
	w = MainWindow()
	w.show()
	icon_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
	tray.attach(w, icon_p)
	return app.exec()

if __name__ == '__main__':
	sys.exit(run())