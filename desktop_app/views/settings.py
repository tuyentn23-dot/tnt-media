# -- coding: utf-8 --
# desktop_app/views/settings.py
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFrame, QTextEdit, QMessageBox, QListWidget, QListWidgetItem, QScrollArea)
from PySide6.QtCore import Qt
import i18n, api
from widgets import PageHeader


class Settings(QWidget):
	def __init__(self, app, parent=None):
		super().__init__(parent)
		self.app = app
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t('nav.settings'), 'Cau hinh he thong')
		root.addWidget(self.header)
		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		scroll.setFrameShape(QFrame.NoFrame)
		inner = QWidget()
		body = QVBoxLayout(inner)
		body.setContentsMargins(20, 16, 20, 16)
		body.setSpacing(12)
		# Card 1
		c1 = QFrame(); c1.setObjectName('Card')
		l1 = QVBoxLayout(c1); l1.setContentsMargins(16, 14, 16, 14); l1.setSpacing(10)
		l1.addWidget(QLabel('<b>Chung</b>'))
		r1 = QHBoxLayout()
		r1.addWidget(QLabel(i18n.t('set.lang')))
		self.lang = QComboBox()
		self.lang.addItems(['Tieng Viet', 'English'])
		self.lang.setCurrentIndex(0 if i18n.get_lang() == 'vi' else 1)
		self.lang.currentIndexChanged.connect(self.on_lang)
		r1.addWidget(self.lang)
		r1.addSpacing(24)
		r1.addWidget(QLabel(i18n.t('set.theme')))
		self.theme = QComboBox()
		self.theme.addItems(['Light', 'Dark', 'System'])
		self.theme.currentIndexChanged.connect(self.on_theme)
		r1.addWidget(self.theme)
		r1.addSpacing(24)
		r1.addWidget(QLabel('API URL:'))
		self.url = QLabel('http://127.0.0.1:7777')
		self.url.setStyleSheet('color:#0A84FF;font-weight:600')
		r1.addWidget(self.url)
		r1.addStretch()
		l1.addLayout(r1)
		body.addWidget(c1)
		# Card 2: credentials
		c2 = QFrame(); c2.setObjectName('Card')
		l2 = QVBoxLayout(c2); l2.setContentsMargins(16, 14, 16, 14); l2.setSpacing(6)
		l2.addWidget(QLabel('<b>Credentials (trang thai)</b>'))
		self.cred = QLabel('Dang kiem tra...')
		self.cred.setStyleSheet('font-family:Consolas;font-size:12px')
		l2.addWidget(self.cred)
		body.addWidget(c2)
		# Card 3: backup
		c3 = QFrame(); c3.setObjectName('Card')
		l3 = QVBoxLayout(c3); l3.setContentsMargins(16, 14, 16, 14); l3.setSpacing(6)
		l3.addWidget(QLabel('<b>Backup DB</b>'))
		r3 = QHBoxLayout()
		b1 = QPushButton(i18n.t('set.backup'))
		b1.clicked.connect(self.do_backup)
		b2 = QPushButton(i18n.t('set.selfcheck'))
		b2.clicked.connect(self.do_selfcheck)
		r3.addWidget(b1); r3.addWidget(b2); r3.addStretch()
		l3.addLayout(r3)
		self.backup_list = QListWidget()
		self.backup_list.setMaximumHeight(120)
		l3.addWidget(self.backup_list)
		body.addWidget(c3)
		# Card 4: advanced
		c4 = QFrame(); c4.setObjectName('Card')
		l4 = QVBoxLayout(c4); l4.setContentsMargins(16, 14, 16, 14); l4.setSpacing(6)
		l4.addWidget(QLabel('<b>Nang cao</b>'))
		r4 = QHBoxLayout()
		b3 = QPushButton('Clear thumbnail cache')
		b3.clicked.connect(self.do_clear_thumb)
		b4 = QPushButton('Reload status')
		b4.clicked.connect(self.refresh_creds)
		r4.addWidget(b3); r4.addWidget(b4); r4.addStretch()
		l4.addLayout(r4)
		body.addWidget(c4)
		# Card 5: Log viewer
		c5 = QFrame(); c5.setObjectName('Card')
		l5 = QVBoxLayout(c5); l5.setContentsMargins(16, 14, 16, 14); l5.setSpacing(6)
		l5.addWidget(QLabel('<b>Xem log</b>'))
		r5 = QHBoxLayout()
		self.log_file = QComboBox()
		self.log_file.setMinimumWidth(220)
		self.log_level = QComboBox()
		self.log_level.addItems(['Tat ca', 'INFO', 'WARN', 'ERROR'])
		b5 = QPushButton('Load')
		b5.clicked.connect(self.do_load_log)
		b6 = QPushButton('Refresh list')
		b6.clicked.connect(self.refresh_log_list)
		r5.addWidget(self.log_file)
		r5.addWidget(self.log_level)
		r5.addWidget(b5); r5.addWidget(b6); r5.addStretch()
		l5.addLayout(r5)
		self.log_view = QTextEdit()
		self.log_view.setReadOnly(True)
		self.log_view.setMinimumHeight(120)
		l5.addWidget(self.log_view)
		body.addWidget(c5)
		lbl = QLabel('Ket qua')
		body.addWidget(lbl)
		self.out = QTextEdit()
		self.out.setReadOnly(True)
		self.out.setMinimumHeight(100)
		body.addWidget(self.out)
		body.addStretch()
		scroll.setWidget(inner)
		root.addWidget(scroll)
		self.refresh_creds()
		self.refresh_backups()
		self.refresh_log_list()

	def on_lang(self, idx):
		i18n.set_lang('vi' if idx == 0 else 'en')
		self.app.rebuild_ui()

	def on_theme(self, idx):
		name = ['light', 'dark', 'light'][idx]
		self.app.set_theme(name)

	def refresh_creds(self):
		try:
			base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
			env = os.path.join(base, '.env')
			keys = []
			if os.path.exists(env):
				for line in open(env, encoding='utf-8', errors='replace'):
					line = line.strip()
					if not line or line.startswith('#') or '=' not in line:
						continue
					k, v = line.split('=', 1)
					v = v.strip()
					v = v.replace(chr(34), '').replace(chr(39), '')
					kl = k.upper()
					if 'KEY' in kl or 'TOKEN' in kl or 'SECRET' in kl:
						masked = (v[:6] + '...' + v[-4:]) if len(v) > 12 else ('SET' if v else 'EMPTY')
						keys.append(k + ' = ' + masked)
			txt = chr(10).join(keys) if keys else '(khong doc duoc .env)'
		except Exception as e:
			txt = 'Loi: ' + str(e)[:100]
		self.cred.setText(txt)

	def refresh_backups(self):
		self.backup_list.clear()
		try:
			d = api.get('/api/backup/list')
			for it in d.get('items', [])[-10:]:
				nm = it.get('name')
				sz = it.get('size', 0)
				self.backup_list.addItem(str(nm) + ' (' + str(int(sz/1024)) + ' KB)')
		except Exception as e:
			self.backup_list.addItem(str(e)[:80])

	def do_backup(self):
		r = api.backup()
		self.out.append('backup: ' + str(r))
		self.refresh_backups()

	def do_selfcheck(self):
		r = api.selfcheck()
		out = r.get('output', str(r))
		self.out.append('selfcheck:')
		self.out.append(out[-1500:] if isinstance(out, str) else str(out)[:1500])

	def refresh_log_list(self):
		self.log_file.clear()
		try:
			d = api.get('/api/diagnostics/logs/list')
			for it in d.get('items', []):
				self.log_file.addItem(it.get('name'))
		except Exception as e:
			self.log_file.addItem(str(e)[:50])
	def do_load_log(self):
		nm = self.log_file.currentText()
		lv = self.log_level.currentText()
		try:
			d = api.get('/api/diagnostics/logs?name=' + nm + '&limit=500')
			lines = d.get('items', [])
		except Exception as e:
			lines = []; self.out.append(str(e)[:80])
		if lv != 'Tat ca':
			lines = [x for x in lines if lv in x]
		self.log_view.setPlainText(chr(10).join(lines[-300:]))
	def do_clear_thumb(self):
		try:
			import shutil
			base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
			d = os.path.join(base, 'state', 'thumb')
			if os.path.isdir(d):
				shutil.rmtree(d)
				self.out.append('Da xoa thumb cache')
			else:
				self.out.append('Khong co cache')
		except Exception as e:
			self.out.append('Loi: ' + str(e)[:100])
