# -- coding: utf-8 --
# desktop_app/views/queue.py
from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox,
	QScrollArea, QFrame, QGridLayout, QDialog, QDialogButtonBox,
	QDateTimeEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDateTime, QUrl
try:
	from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
	from PySide6.QtMultimediaWidgets import QVideoWidget
	HAS_MULTI = True
except Exception:
	HAS_MULTI = False
import i18n, api
from widgets import PageHeader


class VideoDialog(QDialog):
	def __init__(self, pub, parent=None):
		super().__init__(parent)
		self.setWindowTitle('Video #' + str(pub.get('id')))
		self.resize(540, 900)
		lay = QVBoxLayout(self)
		if HAS_MULTI:
			self.player = QMediaPlayer(self)
			self.audio = QAudioOutput(self)
			self.player.setAudioOutput(self.audio)
			vw = QVideoWidget()
			vw.setMinimumSize(500, 700)
			self.player.setVideoOutput(vw)
			lay.addWidget(vw)
			src = QUrl.fromLocalFile(str(pub.get('file_path')))
			self.player.setSource(src)
			self.player.play()
		else:
			lay.addWidget(QLabel('QtMultimedia khong san co'))
		info = QLabel('Channel: ' + str(pub.get('channel_id')) + ' | ' + str(pub.get('kind')))
		lay.addWidget(info)
		btns = QDialogButtonBox(QDialogButtonBox.Close)
		btns.rejected.connect(self.reject)
		lay.addWidget(btns)


class QueueCard(QFrame):
	def __init__(self, pub, onview, onpublish, onschedule, onunschedule, onreject, parent=None):
		super().__init__(parent)
		self.pub = pub
		self.setObjectName('Card')
		self.setFixedWidth(220)
		lay = QVBoxLayout(self)
		lay.setContentsMargins(10, 10, 10, 10)
		lay.setSpacing(6)
		pid = pub.get('id')
		ttl = QLabel(str(pub.get('topic') or pub.get('title') or ('#' + str(pid))))
		ttl.setWordWrap(True)
		ttl.setStyleSheet('font-weight:700;font-size:12px')
		lay.addWidget(ttl)
		meta = QLabel(str(pub.get('channel_id')) + ' | ' + str(pub.get('kind')))
		meta.setStyleSheet('color:#8E8E93;font-size:10px')
		lay.addWidget(meta)
		status = str(pub.get('status'))
		sch = pub.get('schedule_at')
		stag = QLabel(('Lich: ' + str(sch)) if sch else status)
		color = '#0A84FF' if sch else ('#34C759' if status=='rendered' else '#8E8E93')
		stag.setStyleSheet('color:' + color + ';font-size:10px;font-weight:600')
		lay.addWidget(stag)
		r1 = QHBoxLayout()
		b1 = QPushButton('Xem')
		b1.clicked.connect(lambda: onview(pub))
		b2 = QPushButton('Dang ngay')
		b2.setObjectName('Primary')
		b2.clicked.connect(lambda: onpublish(pub))
		r1.addWidget(b1); r1.addWidget(b2)
		lay.addLayout(r1)
		r2 = QHBoxLayout()
		if sch:
			b3 = QPushButton('Huy lich')
			b3.clicked.connect(lambda: onunschedule(pub))
		else:
			b3 = QPushButton('Len lich')
			b3.clicked.connect(lambda: onschedule(pub))
		b4 = QPushButton('Bo')
		b4.clicked.connect(lambda: onreject(pub))
		r2.addWidget(b3); r2.addWidget(b4)
		lay.addLayout(r2)


class Queue(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t('nav.queue'), i18n.t('queue.sub'))
		root.addWidget(self.header)
		body = QVBoxLayout()
		body.setContentsMargins(20, 16, 20, 16)
		body.setSpacing(10)
		bar = QHBoxLayout()
		bar.addWidget(QLabel('Kenh:'))
		self.fch = QComboBox(); self.fch.addItem('Tat ca', None)
		bar.addWidget(self.fch)
		bar.addSpacing(12)
		bar.addWidget(QLabel('Trang thai:'))
		self.fst = QComboBox()
		self.fst.addItem('Chua len lich', 'rendered')
		self.fst.addItem('Da len lich', 'scheduled')
		self.fst.addItem('Da duyet', 'approved')
		self.fst.addItem('Tat ca', None)
		bar.addWidget(self.fst)
		bar.addSpacing(12)
		self.btnreload = QPushButton(i18n.t('btn.refresh'))
		self.btnreload.clicked.connect(self.refresh)
		bar.addWidget(self.btnreload)
		bar.addStretch()
		self.count = QLabel('')
		bar.addWidget(self.count)
		body.addLayout(bar)
		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)
		self.container = QWidget()
		self.grid = QGridLayout(self.container)
		self.grid.setSpacing(12)
		self.scroll.setWidget(self.container)
		body.addWidget(self.scroll, 1)
		root.addLayout(body)
		self.fch.currentIndexChanged.connect(self.refresh)
		self.fst.currentIndexChanged.connect(self.refresh)
		self.loadchannels()
		self.refresh()

	def loadchannels(self):
		try:
			d = api.channels()
			items = d.get('channels', d.get('items', []))
		except Exception:
			items = []
		for it in items:
			if isinstance(it, dict):
				self.fch.addItem(str(it.get('id')), it.get('id'))

	def _clear(self):
		while self.grid.count():
			w = self.grid.takeAt(0).widget()
			if w:
				w.deleteLater()

	def refresh(self):
		self._clear()
		ch = self.fch.currentData()
		st = self.fst.currentData()
		try:
			d = api.publications_queue(status=st, channel_id=ch)
		except Exception as e:
			self.count.setText('Loi: ' + str(e)); return
		items = d.get('items', [])
		self.count.setText(str(len(items)) + ' video')
		for i, pub in enumerate(items):
			card = QueueCard(pub, self._view, self._publish, self._schedule, self._unschedule, self._reject)
			self.grid.addWidget(card, i // 5, i % 5)
		if not items:
			self.grid.addWidget(QLabel('Khong co video trong hang doi'), 0, 0)

	def _view(self, pub):
		VideoDialog(pub, self).exec()

	def _publish(self, pub):
		pid = pub.get('id')
		if QMessageBox.question(self, 'Dang', 'Dang video #' + str(pid) + '?') != QMessageBox.Yes: return
		r = api.publish_pub(pid)
		QMessageBox.information(self, 'Ket qua', str(r)[:400])
		self.refresh()

	def _schedule(self, pub):
		pid = pub.get('id')
		dlg = QDialog(self); dlg.setWindowTitle('Len lich #' + str(pid))
		v = QVBoxLayout(dlg)
		v.addWidget(QLabel('Chon thoi gian:'))
		de = QDateTimeEdit(QDateTime.currentDateTime().addSecs(3600))
		de.setCalendarPopup(True)
		de.setDisplayFormat('yyyy-MM-dd HH:mm')
		v.addWidget(de)
		bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject)
		v.addWidget(bb)
		if dlg.exec() != QDialog.Accepted: return
		at = de.dateTime().toString('yyyy-MM-dd HH:mm')
		r = api.schedule_pub(pid, at)
		QMessageBox.information(self, 'Ket qua', str(r)[:300])
		self.refresh()

	def _unschedule(self, pub):
		pid = pub.get('id')
		r = api.unschedule_pub(pid)
		QMessageBox.information(self, 'Ket qua', str(r)[:300])
		self.refresh()

	def _reject(self, pub):
		pid = pub.get('id')
		if QMessageBox.question(self, 'Bo', 'Bo video #' + str(pid) + '?') != QMessageBox.Yes: return
		api.reject(pid)
		self.refresh()
