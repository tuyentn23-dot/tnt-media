# -- coding: utf-8 --
# desktop_app/views/dashboard.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, QTimer
import i18n, api
from widgets import Card, PageHeader
try:
	from PySide6.QtCharts import QChart, QChartView, QLineSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
	from PySide6.QtGui import QPainter, QPen, QColor
	HAS_CHARTS = True
except Exception:
	HAS_CHARTS = False


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
		# Row 1: 6 KPI cards
		grid = QGridLayout()
		grid.setSpacing(12)
		self.c_pubs = Card('Tong video', '?')
		self.c_views = Card('Luot xem', '?')
		self.c_likes = Card('Luot thich', '?')
		self.c_pub = Card('Da dang', '?')
		self.c_sched = Card('Da len lich', '?')
		self.c_server = Card('Server', '?')
		grid.addWidget(self.c_pubs, 0, 0)
		grid.addWidget(self.c_views, 0, 1)
		grid.addWidget(self.c_likes, 0, 2)
		grid.addWidget(self.c_pub, 0, 3)
		grid.addWidget(self.c_sched, 0, 4)
		grid.addWidget(self.c_server, 0, 5)
		body.addLayout(grid)
		# Chart
		if HAS_CHARTS:
			self.chart = QChart()
			self.chart.setTitle('7 ngay gan nhat')
			self.chart.setAnimationOptions(QChart.SeriesAnimations)
			self.chart.legend().setVisible(True)
			self.chartview = QChartView(self.chart)
			self.chartview.setRenderHint(QPainter.Antialiasing)
			self.chartview.setMinimumHeight(220)
			body.addWidget(self.chartview)
		# Table
		lbl = QLabel(i18n.t('dash.recent'))
		lbl.setObjectName('CardTitle')
		body.addWidget(lbl)
		self.table = QTableWidget(0, 6)
		self.table.setHorizontalHeaderLabels(['ID', 'Kenh', 'Tieu de', 'Trang thai', 'Views', 'Ngay'])
		self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
		self.table.verticalHeader().setVisible(False)
		self.table.setEditTriggers(QTableWidget.NoEditTriggers)
		self.table.setSelectionBehavior(QTableWidget.SelectRows)
		self.table.setAlternatingRowColors(True)
		body.addWidget(self.table)
		root.addLayout(body)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.refresh)
		self.timer.start(10000)
		self.refresh()

	def refresh(self):
		try:
			h = api.health()
		except Exception:
			h = {}
		if h.get('ok'):
			self.c_server.set('ON', '127.0.0.1:7777')
		else:
			self.c_server.set('OFF', '')
		try:
			ds = api.get('/api/dashboard/stats')
		except Exception:
			ds = {}
		summ = ds.get('summary') or {}
		self.c_pubs.set(str(summ.get('pubs', 0)), 'video')
		self.c_views.set(str(summ.get('views', 0)), 'tong')
		self.c_likes.set(str(summ.get('likes', 0)), 'tong')
		self.c_pub.set(str(summ.get('published', 0)), 'youtube')
		self.c_sched.set(str(summ.get('scheduled', 0)), 'cho')
		# Chart update
		if HAS_CHARTS:
			days = ds.get('days') or []
			self._update_chart(days)
		# Table
		data = api.publications()
		items = data.get('items', [])
		self.table.setRowCount(0)
		for it in items[:15]:
			r = self.table.rowCount()
			self.table.insertRow(r)
			self.table.setItem(r, 0, QTableWidgetItem(str(it.get('id', ''))))
			self.table.setItem(r, 1, QTableWidgetItem(str(it.get('channel_id', ''))))
			self.table.setItem(r, 2, QTableWidgetItem(str(it.get('title') or it.get('topic') or '')))
			self.table.setItem(r, 3, QTableWidgetItem(str(it.get('status', ''))))
			self.table.setItem(r, 4, QTableWidgetItem(str(it.get('view_count', 0))))
			self.table.setItem(r, 5, QTableWidgetItem(str(it.get('published_at') or it.get('created_at') or '')))

	def _update_chart(self, days):
		self.chart.removeAllSeries()
		for a in list(self.chart.axes()):
			self.chart.removeAxis(a)
		series = QLineSeries()
		series.setName('Views')
		cats = []
		mx = 1
		for i, d in enumerate(days):
			v = int(d.get('views', 0))
			series.append(i, v)
			cats.append(str(d.get('date', ''))[5:])
			if v > mx:
				mx = v
		pen = QPen(QColor(10, 132, 255))
		pen.setWidth(2)
		series.setPen(pen)
		self.chart.addSeries(series)
		ax = QValueAxis()
		ax.setRange(0, max(mx, 10))
		ax.setLabelFormat('%d')
		self.chart.addAxis(ax, Qt.AlignLeft)
		series.attachAxis(ax)
		bx = QBarCategoryAxis()
		bx.append(cats)
		self.chart.addAxis(bx, Qt.AlignBottom)
		series.attachAxis(bx)
