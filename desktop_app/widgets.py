# -- coding: utf-8 --
# desktop_app/widgets.py - iOS-style reusable components
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
	QSizePolicy, QPushButton, QWidget, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


def shadow(w, blur=18, y=2, alpha=18):
	e = QGraphicsDropShadowEffect(w)
	e.setBlurRadius(blur)
	e.setOffset(0, y)
	e.setColor(QColor(0, 0, 0, alpha))
	w.setGraphicsEffect(e)
	return e


class GroupCard(QFrame):
	def __init__(self, title=None, parent=None):
		super().__init__(parent)
		self.setObjectName(chr(71)+chr(114)+chr(111)+chr(117)+chr(112))
		self.v = QVBoxLayout(self)
		self.v.setContentsMargins(0, 0, 0, 0)
		self.v.setSpacing(0)
		self._title = title
		if title:
			h = QLabel(title.upper())
			h.setObjectName(chr(83)+chr(101)+chr(99)+chr(116)+chr(105)+chr(111)+chr(110)+chr(84)+chr(105)+chr(116)+chr(108)+chr(101))
			h.setContentsMargins(16, 14, 16, 6)
			self.v.addWidget(h)

	def _sep(self):
		s = QFrame()
		s.setObjectName(chr(82)+chr(111)+chr(119)+chr(83)+chr(101)+chr(112))
		s.setFixedHeight(1)
		self.v.addWidget(s)

	def _need_sep(self):
		return self.v.count() > (1 if self._title else 0)

	def add(self, widget, pad=(12, 10, 12, 10)):
		if self._need_sep():
			self._sep()
		box = QWidget()
		bl = QHBoxLayout(box)
		bl.setContentsMargins(*pad)
		bl.setSpacing(10)
		if isinstance(widget, QWidget):
			bl.addWidget(widget)
		else:
			bl.addLayout(widget)
		self.v.addWidget(box)
		return box

	def add_row(self, label, control=None, hint=None):
		if self.need_sep():
			self.sep()
		box = QWidget()
		bl = QHBoxLayout(box)
		bl.setContentsMargins(16, 10, 16, 10)
		bl.setSpacing(10)
		col = QVBoxLayout()
		col.setSpacing(2)
		lbl = QLabel(label)
		lbl.setObjectName(chr(70)+chr(105)+chr(101)+chr(108)+chr(100)+chr(76)+chr(97)+chr(98)+chr(101)+chr(108))
		col.addWidget(lbl)
		if hint:
			h = QLabel(hint)
			h.setObjectName(chr(67)+chr(97)+chr(114)+chr(100)+chr(83)+chr(117)+chr(98))
			col.addWidget(h)
		bl.addLayout(col)
		bl.addStretch()
		if control is not None:
			if isinstance(control, QWidget):
				control.setMinimumWidth(160)
				bl.addWidget(control)
			else:
				bl.addLayout(control)
		self.v.addWidget(box)
		return box


class PageHeader(QWidget):
	def __init__(self, title, sub='', actions=None):
		super().__init__()
		self.setObjectName(chr(84)+chr(111)+chr(112)+chr(66)+chr(97)+chr(114))
		h = QHBoxLayout(self)
		h.setContentsMargins(20, 14, 20, 14)
		h.setSpacing(12)
		col = QVBoxLayout()
		col.setSpacing(2)
		t = QLabel(title)
		t.setObjectName(chr(80)+chr(97)+chr(103)+chr(101)+chr(84)+chr(105)+chr(116)+chr(108)+chr(101))
		col.addWidget(t)
		if sub:
			s = QLabel(sub)
			s.setObjectName(chr(80)+chr(97)+chr(103)+chr(101)+chr(83)+chr(117)+chr(98))
			col.addWidget(s)
		h.addLayout(col)
		h.addStretch()
		self.actions = []
		if actions:
			for a in actions:
				self.add_action(a)

	def add_action(self, btn):
		self.actions.append(btn)
		self.layout().addWidget(btn)
		return btn


class Card(QFrame):
	def __init__(self, title='', value='', sub='', accent=None, parent=None):
		super().__init__(parent)
		self.setObjectName(chr(67)+chr(97)+chr(114)+chr(100))
		v = QVBoxLayout(self)
		v.setContentsMargins(16, 14, 16, 14)
		v.setSpacing(4)
		self.title = QLabel(title)
		self.title.setObjectName(chr(67)+chr(97)+chr(114)+chr(100)+chr(84)+chr(105)+chr(116)+chr(108)+chr(101))
		self.value = QLabel(str(value))
		self.value.setObjectName(chr(67)+chr(97)+chr(114)+chr(100)+chr(86)+chr(97)+chr(108)+chr(117)+chr(101))
		self.sub = QLabel(sub)
		self.sub.setObjectName(chr(67)+chr(97)+chr(114)+chr(100)+chr(83)+chr(117)+chr(98))
		v.addWidget(self.title)
		v.addWidget(self.value)
		v.addWidget(self.sub)
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

	def set(self, value, sub=None):
		self.value.setText(str(value))
		if sub is not None:
			self.sub.setText(str(sub))

	def set_value(self, v):
		self.value.setText(str(v))

	def set_sub(self, s):
		self.sub.setText(str(s))


def busy_wrap(parent, fn, msg='Dang xu ly...'):
	from PySide6.QtWidgets import QApplication
	from PySide6.QtGui import QCursor
	from PySide6.QtCore import Qt
	try:
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		QApplication.processEvents()
	except Exception:
		pass
	try:
		return fn()
	except Exception as e:
		print('[busy_wrap]', e)
		try:
			from PySide6.QtWidgets import QMessageBox
			QMessageBox.warning(parent, 'Loi', str(e)[:400])
		except Exception:
			pass
		return {'ok': False, 'error': str(e)[:300]}
	finally:
		try:
			QApplication.restoreOverrideCursor()
		except Exception:
			pass


class Stepper(QFrame):
	def __init__(self, steps, parent=None):
		super().__init__(parent)
		self.setObjectName('Group')
		self.dots = []
		self.steps = steps
		row = QHBoxLayout(self)
		row.setContentsMargins(20, 18, 20, 18)
		row.setSpacing(0)
		for i, s in enumerate(steps):
			col = QVBoxLayout()
			col.setSpacing(6)
			dot = QLabel(str(i))
			dot.setFixedSize(24, 24)
			dot.setAlignment(Qt.AlignCenter)
			col.addWidget(dot, 0, Qt.AlignHCenter)
			name = s.get('name') if isinstance(s, dict) else s
			lbl = QLabel(name)
			lbl.setAlignment(Qt.AlignHCenter)
			lbl.setStyleSheet('font-size:11px;color:#8E8E93;font-weight:500')
			col.addWidget(lbl)
			self.dots.append(dot)
			row.addLayout(col)
			if i < len(steps) - 1:
				line = QFrame()
				line.setFixedHeight(2)
				line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
				line.setStyleSheet('background:#E5E5EA')
				row.addWidget(line, 0)
		self.set_state(0, 'idle')

	def set_state(self, idx, state, color='#0A84FF'):
		for i, d in enumerate(self.dots):
			if i < idx:
				self._style(d, 'done', '#34C759')
			elif i == idx:
				self._style(d, 'active', color)
			else:
				self._style(d, 'idle', None)

	def _style(self, d, state, color):
		if state == 'done':
			d.setText('✓')
			d.setStyleSheet('background:' + color + ';color:#FFFFFF;border-radius:12px;font-size:11px;font-weight:700')
		elif state == 'active':
			d.setStyleSheet('background:' + color + ';color:#FFFFFF;border-radius:12px;font-size:11px;font-weight:700')
		else:
			d.setStyleSheet('background:#FFFFFF;color:#8E8E93;border:2px solid #C7C7CC;border-radius:12px;font-size:11px;font-weight:700')
