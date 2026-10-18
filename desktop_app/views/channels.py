# -- coding: utf-8 --
# desktop_app/views/channels.py - Redesign v2: card grid
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
	QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
	QDialogButtonBox, QMessageBox, QScrollArea, QFrame, QGridLayout)
from PySide6.QtCore import Qt
import i18n, api
from widgets_v2 import PrimaryButton, SmallButton, DangerButton, StatusBadge


class AddChannelDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle(i18n.t('ch.form_title'))
		self.setMinimumWidth(420)
		form = QFormLayout(self)
		self.fid = QLineEdit()
		self.fid.setPlaceholderText(i18n.t('ch.id_hint'))
		form.addRow(i18n.t('ch.id') + ':', self.fid)
		self.fniche = QLineEdit()
		form.addRow(i18n.t('ch.niche') + ':', self.fniche)
		self.fkinds = QComboBox()
		self.fkinds.addItems(['short', 'long', 'both'])
		form.addRow(i18n.t('ch.kinds') + ':', self.fkinds)
		self.fvoice = QLineEdit()
		self.fvoice.setPlaceholderText('vi-VN-HoaiMyNeural')
		form.addRow(i18n.t('ch.voice') + ':', self.fvoice)
		self.fmaxlen = QSpinBox()
		self.fmaxlen.setRange(5, 600)
		self.fmaxlen.setValue(60)
		form.addRow(i18n.t('ch.max_len') + ':', self.fmaxlen)
		self.fstyle = QLineEdit()
		form.addRow(i18n.t('ch.style') + ':', self.fstyle)
		self.fmode = QComboBox()
		self.fmode.addItems([i18n.t('pipe.auto'), i18n.t('pipe.manual')])
		form.addRow(i18n.t('ch.publish_mode') + ':', self.fmode)
		btn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		btn.accepted.connect(self.accept)
		btn.rejected.connect(self.reject)
		form.addRow(btn)

	def set_data(self, c):
		self.fid.setText(str(c.get('id') or ''))
		self.fid.setReadOnly(True)
		self.fniche.setText(str(c.get('niche') or ''))
		k = c.get('kinds')
		if isinstance(k, list):
			k = ','.join(str(x) for x in k)
		idx = self.fkinds.findText(str(k))
		if idx >= 0:
			self.fkinds.setCurrentIndex(idx)
		st = c.get('style') or {}
		if isinstance(st, dict):
			self.fvoice.setText(str(st.get('voice') or ''))
		if c.get('max_length_sec'):
			self.fmaxlen.setValue(int(c.get('max_length_sec')))
		pm = c.get('publish_mode')
		self.fmode.setCurrentIndex(0 if pm == 'auto' else 1)

	def data(self):
		d = {}
		d['id'] = self.fid.text().strip()
		d['niche'] = self.fniche.text()
		d['kinds'] = self.fkinds.currentText()
		d['voice'] = self.fvoice.text()
		d['max_length_sec'] = self.fmaxlen.value()
		d['style'] = self.fstyle.text()
		d['publish_mode'] = 'auto' if self.fmode.currentIndex() == 0 else 'approve'
		return d


class ChannelCard(QFrame):
	def __init__(self, data, on_edit, on_del, parent=None):
		super().__init__(parent)
		self.data = data
		self.setObjectName('Card')
		self.setMinimumWidth(260)
		self.setMaximumWidth(360)
		v = QVBoxLayout(self)
		v.setContentsMargins(16, 16, 16, 16)
		v.setSpacing(10)

		cid = str(data.get('id') or '')
		hdr = QHBoxLayout()
		av = QLabel(cid[:1].upper() if cid else '?')
		av.setFixedSize(44, 44)
		av.setAlignment(Qt.AlignCenter)
		av.setStyleSheet('background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #FFB6C1,stop:1 #FF69B4);border-radius:22px;color:white;font-size:18px;font-weight:700')
		hdr.addWidget(av)
		names = QVBoxLayout()
		names.setSpacing(2)
		nm = QLabel(cid)
		nm.setStyleSheet('font-size:14px;font-weight:700')
		names.addWidget(nm)
		nid = QLabel('@' + cid.lower())
		nid.setStyleSheet('font-size:11px;color:#8E8E93')
		names.addWidget(nid)
		hdr.addLayout(names, 1)
		v.addLayout(hdr)

		stats = QHBoxLayout()
		stats.setSpacing(0)
		en = data.get('enabled', 1)
		tok = bool(data.get('token'))
		stat_pairs = [
			('Trang thai', 'Hoat dong' if en else 'Tam dung'),
			('Token', 'OK' if tok else 'Thieu'),
			('Kind', str(data.get('kinds') or '')),
		]
		for k, val in stat_pairs:
			col = QVBoxLayout()
			col.setSpacing(2)
			v1 = QLabel(str(val)[:12])
			v1.setAlignment(Qt.AlignCenter)
			v1.setStyleSheet('font-size:12px;font-weight:700')
			col.addWidget(v1)
			l1 = QLabel(k.upper())
			l1.setAlignment(Qt.AlignCenter)
			l1.setStyleSheet('font-size:9px;color:#8E8E93;font-weight:600')
			col.addWidget(l1)
			stats.addLayout(col, 1)
		v.addLayout(stats)

		acts = QHBoxLayout()
		acts.setSpacing(6)
		b1 = SmallButton('Sua')
		b1.clicked.connect(lambda: on_edit(self.data))
		acts.addWidget(b1, 1)
		b2 = SmallButton('Token')
		b2.clicked.connect(lambda: on_edit(self.data))
		acts.addWidget(b2, 1)
		b3 = DangerButton('Xoa')
		b3.setObjectName('SmallButton')
		b3.setStyleSheet('QPushButton{background:#FF453A;color:white;border:1px solid #FF453A;border-radius:8px;padding:0 10px;font-size:11px;min-height:28px;font-weight:600} QPushButton:hover{background:#C41E1E;border-color:#C41E1E}')
		b3.clicked.connect(lambda: on_del(self.data))
		acts.addWidget(b3, 1)
		v.addLayout(acts)


class Channels(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(20, 16, 20, 16)
		root.setSpacing(12)

		hdr = QHBoxLayout()
		title = QLabel('Kenh da ket noi')
		title.setStyleSheet('font-size:22px;font-weight:700')
		hdr.addWidget(title)
		hdr.addStretch()
		self.btn_add = PrimaryButton('+ Them kenh')
		self.btn_add.clicked.connect(self.onadd)
		hdr.addWidget(self.btn_add)
		self.btn_ref = SmallButton('Lam moi')
		self.btn_ref.clicked.connect(self.refresh)
		hdr.addWidget(self.btn_ref)
		root.addLayout(hdr)

		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)
		self.scroll.setFrameShape(QFrame.NoFrame)
		self.container = QWidget()
		self.grid = QGridLayout(self.container)
		self.grid.setContentsMargins(0, 0, 0, 0)
		self.grid.setSpacing(14)
		self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.scroll.setWidget(self.container)
		root.addWidget(self.scroll, 1)

		self.refresh()

	def refresh(self):
		while self.grid.count():
			item = self.grid.takeAt(0)
			if item.widget():
				item.widget().deleteLater()
		try:
			d = api.channels()
			items = d.get('channels', d.get('items', d if isinstance(d, list) else []))
		except Exception:
			items = []
		cards = []
		for it in items:
			if isinstance(it, dict):
				cards.append(it)
		if not cards:
			empty = QLabel('Chua co kenh nao. Bam "+ Them kenh" de bat dau.')
			empty.setStyleSheet('font-size:13px;color:#8E8E93;padding:40px')
			empty.setAlignment(Qt.AlignCenter)
			self.grid.addWidget(empty, 0, 0, 1, 3)
			return
		for i, it in enumerate(cards):
			card = ChannelCard(it, self.onedit, self.ondel)
			self.grid.addWidget(card, i // 3, i % 3)

	def onadd(self):
		dlg = AddChannelDialog(self)
		if dlg.exec() != QDialog.Accepted:
			return
		data = dlg.data()
		if not data.get('id'):
			QMessageBox.warning(self, 'TNT', i18n.t('ch.err_id'))
			return
		r = api.post('/api/channels', data)
		if r.get('ok') is False:
			QMessageBox.warning(self, 'TNT', str(r.get('err', i18n.t('ch.err_exists'))))
		else:
			QMessageBox.information(self, 'TNT', i18n.t('ch.created'))
			self.refresh()

	def onedit(self, ch=None):
		if not ch:
			return
		cid = str(ch.get('id') or '')
		if not cid:
			return
		try:
			d = api.channels()
			items = d.get('channels', d.get('items', []))
			c = next((x for x in items if isinstance(x, dict) and str(x.get('id')) == cid), None)
		except Exception:
			c = None
		if not c:
			QMessageBox.warning(self, 'TNT', 'Khong load duoc kenh')
			return
		dlg = AddChannelDialog(self)
		dlg.setWindowTitle('Sua kenh ' + cid)
		dlg.set_data(c)
		if dlg.exec() != QDialog.Accepted:
			return
		data = dlg.data()
		data.pop('id', None)
		r = api.post('/api/channels/' + cid + '/update', data)
		if r.get('ok'):
			QMessageBox.information(self, 'TNT', 'Da cap nhat')
			self.refresh()
		else:
			QMessageBox.warning(self, 'TNT', str(r)[:200])

	def ondel(self, ch=None):
		if not ch:
			return
		cid = str(ch.get('id') or '')
		if not cid:
			return
		ans = QMessageBox.question(self, 'TNT', i18n.t('ch.confirm_del') + chr(10) + cid)
		if ans != QMessageBox.Yes:
			return
		r = api.delete('/api/channels/' + cid)
		if r.get('ok') is not False:
			QMessageBox.information(self, 'TNT', i18n.t('ch.deleted'))
			self.refresh()
