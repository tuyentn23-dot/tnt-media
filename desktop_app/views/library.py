# -- coding: utf-8 --
# desktop_app/views/library.py - Library: Publications / Jobs / Modules / Trends
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
	QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QComboBox, QLineEdit)
from PySide6.QtCore import Qt
import sqlite3
import i18n, api
from widgets_v2 import (PrimaryButton, SmallButton, StatusBadge)


class TrendsTable(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(12)

		bar = QHBoxLayout()
		bar.setSpacing(8)
		self.search = QLineEdit()
		self.search.setPlaceholderText('Tìm chủ đề...')
		self.search.textChanged.connect(self._filter)
		bar.addWidget(self.search, 1)
		self.kind_filter = QComboBox()
		self.kind_filter.addItem('Tất cả loại', None)
		self.kind_filter.currentIndexChanged.connect(self._filter)
		bar.addWidget(self.kind_filter)
		self.btn_collect = PrimaryButton('Thu thập mới')
		self.btn_collect.clicked.connect(self._collect)
		bar.addWidget(self.btn_collect)
		self.btn_refresh = SmallButton('Làm mới')
		self.btn_refresh.clicked.connect(self.refresh)
		bar.addWidget(self.btn_refresh)
		root.addLayout(bar)

		self.tbl = QTableWidget()
		self.tbl.setColumnCount(5)
		self.tbl.setHorizontalHeaderLabels(['ID', 'Chủ đề', 'Loại bỏ', 'Score', 'Thời gian'])
		self.tbl.verticalHeader().setVisible(False)
		self.tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tbl.setAlternatingRowColors(True)
		hdr = self.tbl.horizontalHeader()
		hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		hdr.setSectionResizeMode(1, QHeaderView.Stretch)
		hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
		hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
		hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
		root.addWidget(self.tbl, 1)

		self._data = []
		self.refresh()

	def _all_trends(self):
		try:
			db = sqlite3.connect('state/pipeline.db')
			rows = db.execute('SELECT id, topic, kind, score, ts FROM trends ORDER BY score DESC, id DESC LIMIT 500').fetchall()
			db.close()
			return [{'id': r[0], 'topic': r[1] or '', 'kind': r[2] or '', 'score': r[3] or 0, 'ts': r[4] or ''} for r in rows]
		except Exception:
			return []

	def refresh(self):
		self._data = self._all_trends()
		kinds = sorted(set(x['kind'] for x in self._data if x['kind']))
		cur = self.kind_filter.currentData()
		self.kind_filter.blockSignals(True)
		self.kind_filter.clear()
		self.kind_filter.addItem('Tất cả loại', None)
		for k in kinds:
			self.kind_filter.addItem(k, k)
		if cur in kinds:
			idx = self.kind_filter.findData(cur)
			if idx >= 0:
				self.kind_filter.setCurrentIndex(idx)
		self.kind_filter.blockSignals(False)
		self._filter()

	def _filter(self):
		q = self.search.text().strip().lower()
		kd = self.kind_filter.currentData()
		rows = self._data
		if q:
			rows = [r for r in rows if q in r['topic'].lower()]
		if kd:
			rows = [r for r in rows if r['kind'] == kd]
		self.tbl.setRowCount(0)
		self.tbl.setRowCount(len(rows))
		for i, r in enumerate(rows):
			self.tbl.setItem(i, 0, QTableWidgetItem(str(r['id'])))
			self.tbl.setItem(i, 1, QTableWidgetItem(r['topic'][:120]))
			self.tbl.setItem(i, 2, QTableWidgetItem(r['kind']))
			self.tbl.setItem(i, 3, QTableWidgetItem(str(r['score'])))
			self.tbl.setItem(i, 4, QTableWidgetItem(str(r['ts'])[:19]))

	def _collect(self):
		try:
			api.post('/api/trends/collect', {'limit': 30})
		except Exception:
			pass
		self.refresh()


class Library(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		from views.tables import Jobs, Pubs, Modules

		root = QVBoxLayout(self)
		root.setContentsMargins(20, 16, 20, 16)
		root.setSpacing(12)

		# Header
		hdr = QHBoxLayout()
		title_col = QVBoxLayout()
		title_col.setSpacing(2)
		t = QLabel('Thư viện')
		t.setStyleSheet('font-size:22px;font-weight:700')
		title_col.addWidget(t)
		s = QLabel('Video đã đăng, công việc, mô-đun và xu hướng')
		s.setStyleSheet('font-size:12px;color:#8E8E93')
		title_col.addWidget(s)
		hdr.addLayout(title_col)
		hdr.addStretch()
		root.addLayout(hdr)

		# Tab bar (custom buttons)
		self.tab_bar = QHBoxLayout()
		self.tab_bar.setSpacing(0)
		root.addLayout(self.tab_bar)

		# Content stack (QTabWidget for simplicity)
		from PySide6.QtWidgets import QTabWidget
		self.tabs = QTabWidget()
		self.tabs.tabBar().setVisible(False)
		self.tabs.setDocumentMode(True)

		self.pubs = Pubs()
		self.jobs = Jobs()
		self.modules = Modules()
		self.trends = TrendsTable()
		for v in (self.pubs, self.jobs, self.modules):
			try:
				v.header.hide()
			except Exception:
				pass
		self.tabs.addTab(self.pubs, 'Đã đăng')
		self.tabs.addTab(self.jobs, 'Công việc')
		self.tabs.addTab(self.modules, 'Mô-đun')
		self.tabs.addTab(self.trends, 'Trends')
		self.tabs.currentChanged.connect(self._on_tab)
		root.addWidget(self.tabs, 1)

		# Custom tab buttons
		self.tab_buttons = []
		for i, name in enumerate(['Đã đăng', 'Công việc', 'Mô-đun', 'Trends']):
			b = SmallButton(name)
			b.setObjectName('SmallButton')
			b.setCheckable(True)
			b.setCursor(Qt.PointingHandCursor)
			b.clicked.connect(lambda _=False, idx=i: self.tabs.setCurrentIndex(idx))
			self.tab_bar.addWidget(b)
			self.tab_buttons.append(b)
		self.tab_bar.addStretch()
		self._update_tab_style(0)

	def _on_tab(self, idx):
		self._update_tab_style(idx)

	def _update_tab_style(self, idx):
		for i, b in enumerate(self.tab_buttons):
			active = i == idx
			b.setChecked(active)
			if active:
				b.setStyleSheet('QPushButton{background:transparent;color:#0A84FF;border:none;border-bottom:2px solid #0A84FF;padding:10px 16px;font-size:13px;font-weight:600;border-radius:0}')
			else:
				b.setStyleSheet('QPushButton{background:transparent;color:#8E8E93;border:none;border-bottom:2px solid transparent;padding:10px 16px;font-size:13px;font-weight:500;border-radius:0} QPushButton:hover{color:#3A3A3C}')

	def refresh(self):
		try:
			self.tabs.currentWidget().refresh()
		except Exception:
			pass
