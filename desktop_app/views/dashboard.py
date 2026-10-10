# -- coding: utf-8 --
# desktop_app/views/dashboard.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, QTimer
import i18n, api
from widgets import Card, PageHeader

class Dashboard(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t('nav.dashboard'), i18n.t('app.sub'))
		root.addWidget(self.header)
		body = QVBoxLayout()
		body.setContentsMargins(20, 16, 20, 16)
		body.setSpacing(14)
		grid = QGridLayout()
		grid.setSpacing(12)
		self.c_server = Card(i18n.t('dash.server'), '?')
		self.c_sched = Card(i18n.t('dash.scheduler'), '?')
		self.c_integ = Card(i18n.t('dash.integrity'), '?')
		self.c_quota = Card(i18n.t('dash.quota'), '?')
		grid.addWidget(self.c_server, 0, 0)
		grid.addWidget(self.c_sched, 0, 1)
		grid.addWidget(self.c_integ, 0, 2)
		grid.addWidget(self.c_quota, 0, 3)
		body.addLayout(grid)
		lbl = QLabel(i18n.t('dash.recent'))
		lbl.setObjectName('CardTitle')
		body.addWidget(lbl)
		self.table = QTableWidget(0, 5)
		self.table.setHorizontalHeaderLabels(['ID', 'Channel', 'Title', 'Status', 'Date'])
		self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
		self.table.verticalHeader().setVisible(False)
		self.table.setEditTriggers(QTableWidget.NoEditTriggers)
		self.table.setSelectionBehavior(QTableWidget.SelectRows)
		body.addWidget(self.table)
		root.addLayout(body)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.refresh)
		self.timer.start(5000)
		self.refresh()

	def refresh(self):
		try:
			h = api.health()
		except Exception:
			h = {}
		if h.get('ok'):
			self.c_server.set('ON', '127.0.0.1:7777')
		else:
			self.c_server.set('OFF', str(h.get('err', ''))[:30])
		se = h.get('scheduler_error') or {}
		alive = se.get('alive')
		stale = se.get('stale')
		if alive and not stale:
			self.c_sched.set('ON', 'tick ' + str((se.get('last_tick') or ''))[-8:])
		elif alive:
			self.c_sched.set('STALE', 'last: ' + str((se.get('last_tick') or ''))[-8:])
		else:
			self.c_sched.set('OFF', '')
		pubs = h.get('publications', 0)
		jobs = h.get('jobs', 0)
		self.c_server.set('ON', 'pub=' + str(pubs) + ' job=' + str(jobs))
		# Integrity check tu selfcheck
		try:
			rr = api.get('/api/diagnostics/selfcheck', 15)
			out = rr.get('output', '')
			ok = rr.get('ok')
			import re as _re
			m = _re.search(r'(\d+) PASS', out)
			npass = m.group(1) if m else '?'
			self.c_integ.set('OK' if ok else 'FAIL', str(npass) + ' PASS')
		except Exception:
			pass
		try:
			q = api.get('/api/analytics/quota')
			rem = q.get('remaining', q.get('units_total', '?'))
			self.c_quota.set(str(rem), 'con lai')
		except Exception:
			self.c_quota.set('?', '')
		data = api.publications()
		items = data.get('items', data if isinstance(data, list) else [])
		self.table.setRowCount(0)
		for it in items[:15]:
			r = self.table.rowCount()
			self.table.insertRow(r)
			self.table.setItem(r, 0, QTableWidgetItem(str(it.get('id', ''))))
			self.table.setItem(r, 1, QTableWidgetItem(str(it.get('channel_id', ''))))
			self.table.setItem(r, 2, QTableWidgetItem(str(it.get('title') or it.get('topic') or '')))
			st = str(it.get('status', ''))
			self.table.setItem(r, 3, QTableWidgetItem(st))
			self.table.setItem(r, 4, QTableWidgetItem(str(it.get('published_at') or it.get('created_at') or '')))
