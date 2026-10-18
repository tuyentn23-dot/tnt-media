# -- coding: utf-8 --
# desktop_app/views/studio.py - Redesign v2: 2-col flex layout
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
	QPushButton, QFrame, QSplitter, QScrollArea)
from PySide6.QtCore import Qt, QTimer
import i18n, api
from widgets_v2 import StatusStrip, SmallButton


class Studio(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		from views.pipeline import Pipeline
		from views.queue import Queue

		self.pipeline = Pipeline()
		self.queue = Queue()

		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)

		
		# Top status strip
		self.status_strip = StatusStrip()
		self.status_strip.refresh_btn.clicked.connect(self.refresh)
		root.addWidget(self.status_strip)

		# 2-col splitter (pipeline 3, queue 2)
		split = QSplitter(Qt.Horizontal)
		split.setChildrenCollapsible(False)

		left = QWidget()
		ll = QVBoxLayout(left)
		ll.setContentsMargins(0, 0, 0, 0)
		ll.setSpacing(0)
		ll.addWidget(self.pipeline)

		right = QWidget()
		right.setObjectName('RightPanel')
		right.setStyleSheet('#RightPanel{background:#FFFFFF;border-left:1px solid #E5E5EA}')
		rl = QVBoxLayout(right)
		rl.setContentsMargins(0, 0, 0, 0)
		rl.setSpacing(0)
		rl.addWidget(self.queue)

		split.addWidget(left)
		split.addWidget(right)
		split.setStretchFactor(0, 3)
		split.setStretchFactor(1, 2)
		split.setSizes([600, 400])
		self.split = split
		root.addWidget(split, 1)

		# Timer refresh status
		self._t = QTimer(self)
		self._t.timeout.connect(self._refresh_status)
		self._t.start(15000)
		self._refresh_status()

	def _refresh_status(self):
		try:
			h = api.health()
		except Exception:
			h = {}
		self.status_strip.update_health(h)

	def refresh(self):
		self._refresh_status()
		try:
			self.queue.refresh()
		except Exception:
			pass
