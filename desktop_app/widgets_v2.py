# -- coding: utf-8 --
# desktop_app/widgets_v2.py - Redesign v2 helper widgets
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
	QSizePolicy, QPushButton, QWidget, QCheckBox, QGridLayout)
from PySide6.QtCore import Qt, Signal


class PrimaryButton(QPushButton):
	def __init__(self, text='', parent=None):
		super().__init__(text, parent)
		self.setObjectName('Primary')
		self.setCursor(Qt.PointingHandCursor)


class DangerButton(QPushButton):
	def __init__(self, text='', parent=None):
		super().__init__(text, parent)
		self.setObjectName('Danger')
		self.setCursor(Qt.PointingHandCursor)


class SecondaryButton(QPushButton):
	def __init__(self, text='', parent=None):
		super().__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)


class SmallButton(QPushButton):
	def __init__(self, text='', parent=None):
		super().__init__(text, parent)
		self.setObjectName('SmallButton')
		self.setCursor(Qt.PointingHandCursor)


class Card(QFrame):
	def __init__(self, header='', parent=None):
		super().__init__(parent)
		self.setObjectName('Card')
		self._v = QVBoxLayout(self)
		self._v.setContentsMargins(14, 14, 14, 14)
		self._v.setSpacing(10)
		if header:
			lbl = QLabel(header.upper())
			lbl.setObjectName('CardHeader')
			self._v.addWidget(lbl)
		self.body = QVBoxLayout()
		self.body.setSpacing(10)
		self._v.addLayout(self.body)

	def add(self, w):
		if isinstance(w, QWidget):
			self.body.addWidget(w)
		else:
			self.body.addLayout(w)


class FieldRow(QWidget):
	def __init__(self, label, control, parent=None):
		super().__init__(parent)
		self.control = control
		v = QVBoxLayout(self)
		v.setContentsMargins(0, 0, 0, 0)
		v.setSpacing(4)
		self.lbl = QLabel(label)
		self.lbl.setObjectName('FieldLabel')
		v.addWidget(self.lbl)
		if isinstance(control, QWidget):
			v.addWidget(control)
		else:
			v.addLayout(control)

	def setVisible(self, vis):
		super().setVisible(vis)
		try:
			self.lbl.setVisible(vis)
		except Exception:
			pass


class FieldGrid(QWidget):
	def __init__(self, cols=3, hgap=12, vgap=10, parent=None):
		super().__init__(parent)
		self.cols = cols
		self.g = QGridLayout(self)
		self.g.setContentsMargins(0, 0, 0, 0)
		self.g.setHorizontalSpacing(hgap)
		self.g.setVerticalSpacing(vgap)
		self._i = 0
		for c in range(cols):
			self.g.setColumnStretch(c, 1)

	def add(self, label, control):
		row = self._i // self.cols
		col = self._i % self.cols
		fr = FieldRow(label, control)
		self.g.addWidget(fr, row, col)
		self._i += 1
		return fr

	def add_span(self, widget):
		row = self._i // self.cols
		self.g.addWidget(widget, row, 0, 1, self.cols)
		self._i = row * self.cols + self.cols
		return widget

	def add_span_here(self, widget):
		row = self._i // self.cols
		col = self._i % self.cols
		span = self.cols - col
		self.g.addWidget(widget, row, col, 1, span)
		self._i = (row + 1) * self.cols
		return widget


class StatusBadge(QLabel):
	STYLES = {
		'success': 'background:#E5F9EB;color:#1B9E3E',
		'danger': 'background:#FEE5E3;color:#C41E1E',
		'warn': 'background:#FFF2DF;color:#B86E00',
		'info': 'background:#E5F1FE;color:#0A66C2',
		'neutral': 'background:#F2F2F7;color:#6C6C70',
	}
	def __init__(self, text, kind='neutral', parent=None):
		super().__init__(str(text).upper(), parent)
		css = self.STYLES.get(kind, self.STYLES['neutral'])
		self.setStyleSheet(css + ';padding:2px 6px;border-radius:4px;font-size:9px;font-weight:700')
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)


class EmptyState(QWidget):
	def __init__(self, icon='', title='', hint='', action=None, parent=None):
		super().__init__(parent)
		v = QVBoxLayout(self)
		v.setContentsMargins(40, 40, 40, 40)
		v.setSpacing(10)
		v.addStretch()
		if icon:
			i = QLabel(icon)
			i.setStyleSheet('font-size:56px')
			i.setAlignment(Qt.AlignCenter)
			v.addWidget(i)
		if title:
			t = QLabel(title)
			t.setStyleSheet('font-size:14px;font-weight:600;color:#3A3A3C')
			t.setAlignment(Qt.AlignCenter)
			v.addWidget(t)
		if hint:
			h = QLabel(hint)
			h.setStyleSheet('font-size:12px;color:#8E8E93')
			h.setAlignment(Qt.AlignCenter)
			h.setWordWrap(True)
			v.addWidget(h)
		if action:
			h2 = QHBoxLayout()
			h2.addStretch()
			h2.addWidget(action)
			h2.addStretch()
			v.addLayout(h2)
		v.addStretch()


class CheckboxRow(QWidget):
	def __init__(self, items, parent=None):
		super().__init__(parent)
		h = QHBoxLayout(self)
		h.setContentsMargins(0, 4, 0, 0)
		h.setSpacing(20)
		self.boxes = {}
		for key, label, checked in items:
			cb = QCheckBox(label)
			cb.setChecked(bool(checked))
			self.boxes[key] = cb
			h.addWidget(cb)
		h.addStretch()

	def is_checked(self, key):
		return self.boxes[key].isChecked() if key in self.boxes else False


class TimelineStep(QWidget):
	STATE_IDLE = 'idle'
	STATE_RUNNING = 'running'
	STATE_DONE = 'done'
	STATE_ERROR = 'error'

	def __init__(self, num, label, parent=None):
		super().__init__(parent)
		self._state = self.STATE_IDLE
		v = QVBoxLayout(self)
		v.setContentsMargins(0, 0, 0, 0)
		v.setSpacing(6)
		v.setAlignment(Qt.AlignHCenter)
		self.dot = QLabel(str(num))
		self.dot.setFixedSize(26, 26)
		self.dot.setAlignment(Qt.AlignCenter)
		v.addWidget(self.dot, 0, Qt.AlignHCenter)
		self.label = QLabel(label)
		self.label.setAlignment(Qt.AlignCenter)
		v.addWidget(self.label)
		self._apply()

	def _apply(self):
		if self._state == self.STATE_DONE:
			self.dot.setText('✓')
			self.dot.setStyleSheet('background:#34C759;color:white;border-radius:13px;font-size:12px;font-weight:700;border:none')
			self.label.setStyleSheet('font-size:10px;color:#3A3A3C;font-weight:500')
		elif self._state == self.STATE_RUNNING:
			self.dot.setStyleSheet('background:#0A84FF;color:white;border-radius:13px;font-size:11px;font-weight:700;border:none')
			self.label.setStyleSheet('font-size:10px;color:#0A84FF;font-weight:700')
		elif self._state == self.STATE_ERROR:
			self.dot.setText('!')
			self.dot.setStyleSheet('background:#FF453A;color:white;border-radius:13px;font-size:12px;font-weight:700;border:none')
			self.label.setStyleSheet('font-size:10px;color:#FF453A;font-weight:600')
		else:
			self.dot.setStyleSheet('background:#FFFFFF;color:#8E8E93;border:2px solid #C7C7CC;border-radius:13px;font-size:11px;font-weight:700')
			self.label.setStyleSheet('font-size:10px;color:#8E8E93;font-weight:500')

	def set_state(self, state):
		self._state = state
		self._apply()


class Timeline(QWidget):
	def __init__(self, steps, parent=None):
		super().__init__(parent)
		h = QHBoxLayout(self)
		h.setContentsMargins(20, 8, 20, 8)
		h.setSpacing(0)
		self.steps = []
		self.lines = []
		for i, (num, label) in enumerate(steps):
			st = TimelineStep(num, label)
			self.steps.append(st)
			h.addWidget(st, 0)
			if i < len(steps) - 1:
				line = QFrame()
				line.setFixedHeight(2)
				line.setMinimumWidth(30)
				line.setStyleSheet('background:#E5E5EA;border:none')
				line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
				self.lines.append(line)
				h.addWidget(line, 1)

	def set_state(self, idx, state):
		for i, st in enumerate(self.steps):
			if i < idx:
				st.set_state(TimelineStep.STATE_DONE)
			elif i == idx:
				st.set_state(state)
			else:
				st.set_state(TimelineStep.STATE_IDLE)

	def reset(self):
		for st in self.steps:
			st.set_state(TimelineStep.STATE_IDLE)


class QueueRow(QFrame):
	clicked = Signal(dict)
	toggled = Signal(dict, bool)
	menu_clicked = Signal(dict)

	def __init__(self, pub, parent=None):
		super().__init__(parent)
		self.pub = pub
		self.setObjectName('QueueItem')
		self.setStyleSheet('#QueueItem{background:white;border:1px solid #E5E5EA;border-radius:8px} #QueueItem:hover{background:#F9F9FC;border-color:#D0D0D8}')
		self.setCursor(Qt.PointingHandCursor)
		h = QHBoxLayout(self)
		h.setContentsMargins(10, 10, 10, 10)
		h.setSpacing(12)
		self.cb = QCheckBox()
		self.cb.setFixedWidth(24)
		self.cb.toggled.connect(lambda c: self.toggled.emit(self.pub, c))
		h.addWidget(self.cb)
		thumb = QLabel('V')
		thumb.setFixedSize(56, 56)
		thumb.setAlignment(Qt.AlignCenter)
		thumb.setStyleSheet('background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #C4D9FF,stop:1 #A8C0FF);border-radius:6px;color:white;font-size:20px;font-weight:700')
		h.addWidget(thumb)
		info = QVBoxLayout()
		info.setSpacing(4)
		title_txt = str(pub.get('topic') or pub.get('title') or ('#' + str(pub.get('id'))))[:80]
		title = QLabel(title_txt)
		title.setStyleSheet('font-size:13px;font-weight:600')
		title.setWordWrap(False)
		from PySide6.QtWidgets import QSizePolicy as _QSP
		title.setSizePolicy(_QSP.Ignored, _QSP.Preferred)
		title.setMinimumWidth(0)
		info.addWidget(title)
		meta = QHBoxLayout()
		meta.setSpacing(6)
		ch = QLabel(str(pub.get('channel_id') or ''))
		ch.setStyleSheet('font-size:10px;color:#8E8E93')
		meta.addWidget(ch)
		st = str(pub.get('status') or '')
		if st == 'published' and pub.get('yt_verified_at'):
			b = StatusBadge('Đã đăng', 'success')
		elif st == 'verify_failed':
			b = StatusBadge('Đã gỡ', 'danger')
		elif st == 'scheduled':
			b = StatusBadge('Hẹn lịch', 'warn')
		elif st in ('rendered', 'approved'):
			b = StatusBadge('Chờ duyệt', 'info')
		else:
			b = StatusBadge(st or '?', 'neutral')
		meta.addWidget(b)
		meta.addStretch()
		info.addLayout(meta)
		h.addLayout(info, 1)
		menu = QLabel('⋯')
		menu.setStyleSheet('font-size:18px;color:#8E8E93;padding:4px 8px')
		menu.setCursor(Qt.PointingHandCursor)
		menu.mousePressEvent = lambda e: self.menu_clicked.emit(self.pub)
		h.addWidget(menu)

	def mousePressEvent(self, e):
		from PySide6.QtWidgets import QApplication
		w = self.childAt(e.pos())
		if w is not None and (isinstance(w, QCheckBox) or w is self.cb):
			super().mousePressEvent(e)
			return
		# Skip if clicked on menu label (⋯)
		try:
			if hasattr(w, "text") and w.text() == chr(8943):
				super().mousePressEvent(e)
				return
		except Exception:
			pass
		self.clicked.emit(self.pub)
		super().mousePressEvent(e)

	def is_checked(self):
		return self.cb.isChecked()

	def set_checked(self, v):
		self.cb.setChecked(v)

class RunButton(PrimaryButton):
	def __init__(self, text="Chay", parent=None):
		super().__init__(text, parent)
		self.setStyleSheet('QPushButton{background:#0A84FF;color:white;border:1px solid #0A84FF;border-radius:8px;padding:0 24px;font-size:14px;font-weight:600;min-height:40px} QPushButton:hover{background:#0066CC;border-color:#0066CC} QPushButton:disabled{background:#B0D4FF;border-color:#B0D4FF}')


class StatusStrip(QFrame):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setObjectName("TopBar")
		self.setFixedHeight(48)
		self.setStyleSheet('#TopBar{background:#FFFFFF;border-bottom:1px solid #E5E5EA}')
		h = QHBoxLayout(self)
		h.setContentsMargins(24, 0, 24, 0)
		h.setSpacing(20)
		self.srv = QLabel('Server')
		self.sch = QLabel('Scheduler')
		self.pub = QLabel('0 video')
		self.job = QLabel('0 job')
		for w in (self.srv, self.sch, self.pub, self.job):
			w.setStyleSheet('font-size:12px;font-weight:600')
			h.addWidget(w)
		h.addStretch()
		self.refresh_btn = SmallButton('Làm mới')
		h.addWidget(self.refresh_btn)

	def update_health(self, h):
		if not isinstance(h, dict):
			h = {}
		if h.get('ok'):
			self.srv.setText(chr(9679) + ' Server ON')
			self.srv.setStyleSheet('color:#34C759;font-size:12px;font-weight:600')
			self.pub.setText(str(h.get('publications', 0)) + ' video')
			self.pub.setStyleSheet('color:#3A3A3C;font-size:12px;font-weight:600')
			self.job.setText(str(h.get('jobs', 0)) + ' job')
			self.job.setStyleSheet('color:#3A3A3C;font-size:12px;font-weight:600')
		else:
			self.srv.setText(chr(9679) + ' Server OFF')
			self.srv.setStyleSheet('color:#FF453A;font-size:12px;font-weight:600')
		se = h.get('scheduler_error') or {}
		if se.get('alive') and not se.get('stale'):
			self.sch.setText(chr(9673) + ' Scheduler chay')
			self.sch.setStyleSheet('color:#0A84FF;font-size:12px;font-weight:600')
		elif se.get('alive'):
			self.sch.setText(chr(9888) + ' Scheduler tre')
			self.sch.setStyleSheet('color:#FF9500;font-size:12px;font-weight:600')
		else:
			self.sch.setText(chr(9675) + ' Scheduler off')
			self.sch.setStyleSheet('color:#8E8E93;font-size:12px;font-weight:600')