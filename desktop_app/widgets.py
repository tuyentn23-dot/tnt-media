# -- coding: utf-8 --
# desktop_app/widgets.py - Reusable Apple-style components
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QApplication, QPushButton
from PySide6.QtCore import Qt, QTimer

class Card(QFrame):
	def __init__(self, title='', value='', parent=None):
		super().__init__(parent)
		self.setObjectName('Card')
		lay = QVBoxLayout(self)
		lay.setContentsMargins(16, 14, 16, 14)
		lay.setSpacing(4)
		self.title = QLabel(title)
		self.title.setObjectName('CardTitle')
		self.value = QLabel(value)
		self.value.setObjectName('CardValue')
		self.sub = QLabel('')
		self.sub.setObjectName('PageSub')
		lay.addWidget(self.title)
		lay.addWidget(self.value)
		lay.addWidget(self.sub)
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

	def set(self, value, sub=None):
		self.value.setText(str(value))
		if sub is not None:
			self.sub.setText(str(sub))

class PageHeader(QFrame):
	def __init__(self, title, sub='', parent=None):
		super().__init__(parent)
		self.setObjectName('TopBar')
		lay = QVBoxLayout(self)
		lay.setContentsMargins(20, 14, 20, 14)
		lay.setSpacing(2)
		self.title = QLabel(title)
		self.title.setObjectName('PageTitle')
		self.sub = QLabel(sub)
		self.sub.setObjectName('PageSub')
		lay.addWidget(self.title)
		lay.addWidget(self.sub)

	def update_text(self, title, sub=''):
		self.title.setText(title)
		self.sub.setText(sub)

def hline():
	f = QFrame()
	f.setFrameShape(QFrame.HLine)
	f.setStyleSheet('color:#E5E5EA')
	return f


def busy_wrap(w, fn, busy_text='Dang xu ly...'):
	'''Chay fn() trong khi disable widget + doi con tro. Tra ve result.'''
	from PySide6.QtGui import QGuiApplication
	had_text = hasattr(w, 'text') and hasattr(w, 'setText')
	orig = w.text() if had_text else ''
	try:
		if w is not None:
			w.setEnabled(False)
		if had_text:
			w.setText(busy_text)
		QGuiApplication.setOverrideCursor(Qt.WaitCursor)
		QApplication.processEvents()
		return fn()
	finally:
		QGuiApplication.restoreOverrideCursor()
		if w is not None:
			w.setEnabled(True)
		if had_text:
			w.setText(orig)

