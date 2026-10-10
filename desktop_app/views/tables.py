# -- coding: utf-8 --
# desktop_app/views/tables.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QAbstractItemView)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
import i18n, api
from widgets import PageHeader


def _val(it, keys, default=''):
	if not isinstance(it, dict):
		return default
	for k in keys:
		if k in it and it[k] is not None:
			return it[k]
	return default


def _items(d):
	if isinstance(d, list):
		return d
	if isinstance(d, dict):
		return d.get('items', d.get('publications', d.get('channels', [])))
	return []


class _Table(QWidget):
	HEADERS = []
	NAVKEY = 'nav.dashboard'
	KEYS = []
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t(self.NAVKEY), '')
		root.addWidget(self.header)
		body = QVBoxLayout()
		body.setContentsMargins(20, 16, 20, 16)
		body.setSpacing(10)
		self.bar = QHBoxLayout()
		self._build_actions(self.bar)
		self.bar.addStretch()
		b = QPushButton(i18n.t('btn.refresh'))
		b.clicked.connect(self.refresh)
		self.bar.addWidget(b)
		body.addLayout(self.bar)
		self.table = QTableWidget(0, len(self.HEADERS))
		self.table.setHorizontalHeaderLabels(self.HEADERS)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setVisible(False)
		self.table.setEditTriggers(QTableWidget.NoEditTriggers)
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.table.setAlternatingRowColors(True)
		body.addWidget(self.table)
		self.msg = QLabel('')
		self.msg.setObjectName('PageSub')
		body.addWidget(self.msg)
		root.addLayout(body)
		self.refresh()

	def _build_actions(self, bar):
		pass

	def _fill(self, rows):
		self.table.setRowCount(0)
		for row in rows:
			r = self.table.rowCount()
			self.table.insertRow(r)
			for c, v in enumerate(row):
				self.table.setItem(r, c, QTableWidgetItem(str(v)))

	def refresh(self):
		rows = []
		for it in _items(self.fetch()):
			rows.append([ _val(it, [k]) for k in self.KEYS])
		self._fill(rows)

	def fetch(self):
		return {}


class Jobs(_Table):
	HEADERS = ['ID', 'Kenh', 'Kind', 'Trang thai', 'Thoi gian (s)', 'Log cuoi', 'Tao luc']
	NAVKEY = 'nav.jobs'
	KEYS = ['id', 'channel_id', 'kind', 'status', 'elapsed_sec', 'log_tail', 'created_at']
	def fetch(self):
		return api.jobs()
	def _fill(self, rows):
		self.table.setRowCount(0)
		for row in rows:
			r = self.table.rowCount()
			self.table.insertRow(r)
			for c, v in enumerate(row):
				if c == 5 and isinstance(v, list):
					txt = v[-1] if v else ''
					self.table.setItem(r, c, QTableWidgetItem(str(txt)[:120]))
				else:
					self.table.setItem(r, c, QTableWidgetItem(str(v)))
	def _build_actions(self, bar):
		self.btn_appr = QPushButton('Duyet')
		self.btn_appr.setObjectName('Primary')
		self.btn_appr.clicked.connect(self.on_approve_multi)
		bar.addWidget(self.btn_appr)
		self.btn_all = QPushButton('Duyet tat ca')
		self.btn_all.clicked.connect(self.on_approve_all)
		bar.addWidget(self.btn_all)
		self.btn_kill = QPushButton('Huy job dang chay')
		self.btn_kill.setObjectName('Danger')
		self.btn_kill.clicked.connect(self.on_kill)
		bar.addWidget(self.btn_kill)
	def on_approve_multi(self):
		rows = sorted(set(i.row() for i in self.table.selectedIndexes()))
		if not rows:
			self.msg.setText('Chon it nhat 1 job')
			return
		ok = 0
		for r in rows:
			jid = self.table.item(r, 0).text()
			res = api.post('/api/jobs/' + str(jid) + '/approve', {})
			if res.get('ok'):
				ok += 1
		self.msg.setText('Da duyet: ' + str(ok) + '/' + str(len(rows)))
		self.refresh()
	def on_approve_all(self):
		r = api.post('/api/jobs/approve_all', {})
		self.msg.setText('Da duyet tat ca: ' + str(r.get('approved', 0)))
		self.refresh()
	def on_kill(self):
		if QMessageBox.question(self, 'Kill', 'Huy tat ca job dang chay?') != QMessageBox.Yes:
			return
		r = api.post('/api/killswitch', {})
		self.msg.setText('Da huy: ' + str(r.get('cancelled', 0)))
		self.refresh()


class Pubs(_Table):
	HEADERS = ['ID', 'Kenh', 'Kind', 'Trang thai', 'YouTube', 'Dang luc']
	NAVKEY = 'nav.pubs'
	KEYS = ['id', 'channel_id', 'kind', 'status', 'youtube_id', 'published_at']
	def fetch(self):
		return api.publications()
	def _build_actions(self, bar):
		self.btn_open = QPushButton('Mo YouTube')
		self.btn_open.setObjectName('Primary')
		self.btn_open.clicked.connect(self.on_open)
		bar.addWidget(self.btn_open)
		self.btn_sync = QPushButton('Sync metrics')
		self.btn_sync.clicked.connect(self.on_sync)
		bar.addWidget(self.btn_sync)
	def on_open(self):
		row = self.table.currentRow()
		if row < 0:
			self.msg.setText('Chon 1 video')
			return
		vid = self.table.item(row, 4).text() if self.table.item(row, 4) else ''
		if not vid or vid == 'None':
			self.msg.setText('Video chua dang YouTube')
			return
		QDesktopServices.openUrl(QUrl('https://youtu.be/' + vid))
		self.msg.setText('Da mo: ' + vid)
	def on_sync(self):
		self.msg.setText('Syncing...')
		r = api.post('/api/metrics/sync', {})
		self.msg.setText('Updated: ' + str(r.get('updated', 0)))
		self.refresh()


class Modules(_Table):
	HEADERS = ['Ten', 'Loai', 'Phien ban', 'Hop le']
	NAVKEY = 'nav.modules'
	KEYS = ['name', 'category', 'version', 'valid']
	def fetch(self):
		return api.modules()
