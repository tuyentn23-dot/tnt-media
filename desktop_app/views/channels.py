# -- coding: utf-8 --
# desktop_app/views/channels.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox, QDialogButtonBox, QMessageBox)
from PySide6.QtCore import Qt
import i18n, api
from widgets import PageHeader

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


class Channels(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t('nav.channels'), '')
		root.addWidget(self.header)
		body = QVBoxLayout()
		body.setContentsMargins(20, 16, 20, 16)
		body.setSpacing(12)
		bar = QHBoxLayout()
		self.btnadd = QPushButton(i18n.t('ch.add'))
		self.btnadd.setObjectName('Primary')
		self.btnadd.clicked.connect(self.onadd)
		bar.addWidget(self.btnadd)
		self.btndel = QPushButton(i18n.t('ch.delete'))
		self.btndel.setObjectName('Danger')
		self.btndel.clicked.connect(self.ondel)
		bar.addWidget(self.btndel)
		bar.addStretch()
		self.btnref = QPushButton(i18n.t('btn.refresh'))
		self.btnref.clicked.connect(self.refresh)
		bar.addWidget(self.btnref)
		body.addLayout(bar)
		self.table = QTableWidget(0, 5)
		self.table.setHorizontalHeaderLabels(['ID', 'Niche', 'Kinds', 'Status', 'Token'])
		self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
		self.table.verticalHeader().setVisible(False)
		self.table.setEditTriggers(QTableWidget.NoEditTriggers)
		self.table.setSelectionBehavior(QTableWidget.SelectRows)
		body.addWidget(self.table)
		root.addLayout(body)
		self.refresh()

	def refresh(self):
		d = api.channels()
		items = d.get('channels', d.get('items', d if isinstance(d, list) else []))
		try:
			sch = api.get('/api/scheduler/status').get('items', [])
		except Exception:
			sch = []
		cron_by = {s.get('channel'): s.get('cron') for s in sch}
		self.table.setRowCount(0)
		for it in items:
			r = self.table.rowCount()
			self.table.insertRow(r)
			if not isinstance(it, dict):
				self.table.setItem(r, 0, QTableWidgetItem(str(it)))
				continue
			cid = str(it.get('id', ''))
			niche = str(it.get('niche') or '')
			kinds = it.get('kinds') or ''
			if isinstance(kinds, list):
				kinds = ','.join(str(k) for k in kinds)
			en = it.get('enabled', 1)
			st = i18n.t('ch.active') if en else i18n.t('ch.paused')
			cron = cron_by.get(cid) or ''
			tok = bool(it.get('token'))
			self.table.setItem(r, 0, QTableWidgetItem(cid))
			self.table.setItem(r, 1, QTableWidgetItem(niche))
			self.table.setItem(r, 2, QTableWidgetItem(kinds))
			self.table.setItem(r, 3, QTableWidgetItem(st + ((chr(32)+chr(124)+chr(32)+cron) if cron else '')))
			self.table.setItem(r, 4, QTableWidgetItem('Y' if tok else 'N'))
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

	def ondel(self):
		row = self.table.currentRow()
		if row < 0:
			return
		cid = self.table.item(row, 0).text()
		ans = QMessageBox.question(self, 'TNT', i18n.t('ch.confirm_del'))
		if ans != QMessageBox.Yes:
			return
		r = api.delete('/api/channels/' + cid)
		if r.get('ok') is not False:
			QMessageBox.information(self, 'TNT', i18n.t('ch.deleted'))
			self.refresh()
