# -*- coding: utf-8 -*-
# desktop_app/views/studio.py - Unified daily workspace.
# Left: Pipeline (single video) / Weekly (batch) tabs. Right: Queue.
# Top: status strip. One screen for the whole daily workflow.
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QSplitter, QTabWidget, QScrollArea
)
from PySide6.QtCore import Qt, QTimer
import i18n, api
from widgets import PageHeader


class StatusStrip(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Group')
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 10, 16, 10)
        lay.setSpacing(20)
        self.srv = QLabel('● Đang kết nối...')
        self.sch = QLabel('○ Scheduler')
        self.pub = QLabel('0 video')
        self.job = QLabel('0 job')
        for w in (self.srv, self.sch, self.pub, self.job):
            w.setStyleSheet('font-size:12px;font-weight:600')
            lay.addWidget(w)
        lay.addStretch()
        self.btn_refresh = QPushButton('Làm mới')
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh)
        lay.addWidget(self.btn_refresh)
        self._t = QTimer(self)
        self._t.timeout.connect(self.refresh)
        self._t.start(15000)
        self.refresh()

    def refresh(self):
        try:
            h = api.health()
        except Exception:
            self.srv.setText('● Mất kết nối')
            self.srv.setStyleSheet('color:#FF453A;font-size:12px;font-weight:600')
            return
        if not isinstance(h, dict):
            h = {}
        if h.get('ok'):
            self.srv.setText('● Server ON')
            self.srv.setStyleSheet('color:#34C759;font-size:12px;font-weight:600')
            self.pub.setText(str(h.get('publications', 0)) + ' video')
            self.job.setText(str(h.get('jobs', 0)) + ' job')
            self.pub.setStyleSheet('color:#3A3A3C;font-size:12px;font-weight:600')
            self.job.setStyleSheet('color:#3A3A3C;font-size:12px;font-weight:600')
        else:
            self.srv.setText('● Server OFF')
            self.srv.setStyleSheet('color:#FF453A;font-size:12px;font-weight:600')
        se = h.get('scheduler_error') or {}
        alive = se.get('alive')
        stale = se.get('stale')
        if alive and not stale:
            self.sch.setText('◉ Scheduler chạy')
            self.sch.setStyleSheet('color:#0A84FF;font-size:12px;font-weight:600')
        elif alive:
            self.sch.setText('⚠ Scheduler trễ')
            self.sch.setStyleSheet('color:#FF9500;font-size:12px;font-weight:600')
        else:
            self.sch.setText('○ Scheduler off')
            self.sch.setStyleSheet('color:#8E8E93;font-size:12px;font-weight:600')


class Studio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from views.pipeline import Pipeline
        from views.queue import Queue
        from views.weekly import Weekly

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = PageHeader(
            i18n.t('nav.studio') if i18n.t('nav.studio') != 'nav.studio' else 'Studio',
            i18n.t('studio.sub') if i18n.t('studio.sub') != 'studio.sub'
            else 'Xưởng sản xuất — Tạo video, hàng đợi, đăng bài'
        )
        root.addWidget(self.header)

        self.status_strip = StatusStrip()
        root.addWidget(self.status_strip)

        self.split = QSplitter(Qt.Horizontal)
        self.split.setChildrenCollapsible(False)

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(8, 8, 4, 8)
        ll.setSpacing(0)
        self.left_tabs = QTabWidget()
        self.pipeline = Pipeline()
        try:
            self.pipeline.header.hide()
        except Exception:
            pass
        self.weekly = Weekly()
        try:
            self.weekly.header.hide()
        except Exception:
            pass
        self.left_tabs.addTab(self.pipeline, 'Tạo 1 video')
        self.left_tabs.addTab(self.weekly, 'Tạo hàng loạt')
        self.left_scroll = QScrollArea()
        self.left_scroll.setWidgetResizable(True)
        self.left_scroll.setFrameShape(QFrame.NoFrame)
        self.left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.left_scroll.setWidget(self.left_tabs)
        ll.addWidget(self.left_scroll)

        self.queue = Queue()
        try:
            self.queue.header.hide()
        except Exception:
            pass
        self.queue.setMinimumWidth(420)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(4, 8, 8, 8)
        rl.setSpacing(0)
        self.queue_scroll = QScrollArea()
        self.queue_scroll.setWidgetResizable(True)
        self.queue_scroll.setFrameShape(QFrame.NoFrame)
        self.queue_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.queue_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.queue_scroll.setWidget(self.queue)
        rl.addWidget(self.queue_scroll)

        self.split.addWidget(left)
        self.split.addWidget(right)
        self.split.setStretchFactor(0, 3)
        self.split.setStretchFactor(1, 2)
        self.split.setSizes([720, 480])
        root.addWidget(self.split, 1)

    def refresh(self):
        try:
            self.status_strip.refresh()
        except Exception:
            pass
        try:
            self.queue.refresh()
        except Exception:
            pass
