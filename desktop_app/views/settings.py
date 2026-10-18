# -- coding: utf-8 --
# desktop_app/views/settings.py - Redesign v2
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
	QPushButton, QComboBox, QFrame, QTextEdit, QMessageBox, QListWidget,
	QScrollArea, QSizePolicy)
from PySide6.QtCore import Qt
import i18n, api
from widgets_v2 import Card, PrimaryButton, SmallButton, DangerButton


class Settings(QWidget):
	def __init__(self, app, parent=None):
		super().__init__(parent)
		self.app = app

		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)

		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		scroll.setFrameShape(QFrame.NoFrame)
		inner = QWidget()
		body = QVBoxLayout(inner)
		body.setContentsMargins(24, 20, 24, 20)
		body.setSpacing(14)
		body.setAlignment(Qt.AlignTop)

		# Header
		hdr = QLabel('Cai dat')
		hdr.setStyleSheet('font-size:22px;font-weight:700')
		body.addWidget(hdr)
		sub = QLabel('Cau hinh he thong TNT Media Studio')
		sub.setStyleSheet('font-size:12px;color:#8E8E93;margin-bottom:4px')
		body.addWidget(sub)

		# Card 1: General
		c1 = Card('Chung')
		self.lang = QComboBox()
		self.lang.addItems(['Tieng Viet', 'English'])
		self.lang.setCurrentIndex(0 if i18n.get_lang() == 'vi' else 1)
		self.lang.currentIndexChanged.connect(self.on_lang)
		self.theme = QComboBox()
		self.theme.addItems(['Sang', 'Toi', 'He thong'])
		self.theme.currentIndexChanged.connect(self.on_theme)
		self.url = QLabel('http://127.0.0.1:7777')
		self.url.setStyleSheet('color:#0A84FF;font-weight:600;font-size:12px')
		row1 = self._row('Ngon ngu', self.lang)
		row2 = self._row('Chu de', self.theme)
		row3 = self._row('API URL', self.url)
		c1.add(row1)
		c1.add(row2)
		c1.add(row3)
		body.addWidget(c1)

		# Card 2: Credentials
		c2 = Card('Credentials (trang thai)')
		self.cred = QLabel('Dang kiem tra...')
		self.cred.setStyleSheet('font-family:Consolas;font-size:12px;color:#3A3A3C')
		self.cred.setWordWrap(True)
		c2.add(self.cred)
		body.addWidget(c2)

		# Card 3: Backup
		c3 = Card('Backup DB')
		r3 = QHBoxLayout()
		r3.setSpacing(6)
		b1 = PrimaryButton(i18n.t('set.backup'))
		b1.clicked.connect(self.do_backup)
		r3.addWidget(b1)
		b2 = SmallButton(i18n.t('set.selfcheck'))
		b2.clicked.connect(self.do_selfcheck)
		r3.addWidget(b2)
		r3.addStretch()
		c3.add(r3)
		self.backup_list = QListWidget()
		self.backup_list.setMaximumHeight(120)
		c3.add(self.backup_list)
		body.addWidget(c3)

		# Card 4: Advanced
		c4 = Card('Nang cao')
		r4 = QHBoxLayout()
		r4.setSpacing(6)
		b3 = SmallButton('Clear thumbnail cache')
		b3.clicked.connect(self.do_clear_thumb)
		r4.addWidget(b3)
		b4 = SmallButton('Reload status')
		b4.clicked.connect(self.refresh_creds)
		r4.addWidget(b4)
		r4.addStretch()
		c4.add(r4)
		body.addWidget(c4)

		# Card 5: Log viewer
		c5 = Card('Xem log')
		r5 = QHBoxLayout()
		r5.setSpacing(6)
		self.log_file = QComboBox()
		self.log_file.setMinimumWidth(200)
		r5.addWidget(self.log_file)
		self.log_level = QComboBox()
		self.log_level.addItems(['Tat ca', 'INFO', 'WARN', 'ERROR'])
		r5.addWidget(self.log_level)
		b5 = SmallButton('Load')
		b5.clicked.connect(self.do_load_log)
		r5.addWidget(b5)
		b6 = SmallButton('Refresh list')
		b6.clicked.connect(self.refresh_log_list)
		r5.addWidget(b6)
		r5.addStretch()
		c5.add(r5)
		self.log_view = QTextEdit()
		self.log_view.setReadOnly(True)
		self.log_view.setMinimumHeight(140)
		c5.add(self.log_view)
		body.addWidget(c5)

		# Card 6: Output
		c6 = Card('Ket qua')
		self.out = QTextEdit()
		self.out.setReadOnly(True)
		self.out.setMinimumHeight(100)
		c6.add(self.out)
		body.addWidget(c6)

		body.addStretch()
		scroll.setWidget(inner)
		root.addWidget(scroll)

		self.refresh_creds()
		self.refresh_backups()
		self.refresh_log_list()

	def _row(self, label, control):
		w = QWidget()
		h = QHBoxLayout(w)
		h.setContentsMargins(0, 0, 0, 0)
		h.setSpacing(10)
		lbl = QLabel(label)
		lbl.setStyleSheet('font-size:12px;color:#3A3A3C;font-weight:500')
		lbl.setFixedWidth(120)
		h.addWidget(lbl)
		if isinstance(control, QWidget):
			control.setMinimumWidth(180)
			h.addWidget(control)
		h.addStretch()
		return w

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
					v = v.strip().replace(chr(34), '').replace(chr(39), '')
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
			lines = []
			self.out.append(str(e)[:80])
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
