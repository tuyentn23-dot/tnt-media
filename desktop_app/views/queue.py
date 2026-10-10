# -- coding: utf-8 --
# desktop_app/views/queue.py - Video Queue
from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox,
	QScrollArea, QFrame, QGridLayout, QDialog, QDialogButtonBox,
	QDateTimeEdit, QMessageBox, QLineEdit, QCheckBox, QPlainTextEdit
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


class EditDialog(QDialog):
	def __init__(self, pub, parent=None):
		super().__init__(parent)
		self.pub = pub
		self.setWindowTitle('Sua metadata #' + str(pub.get('id')))
		self.resize(520, 420)
		lay = QVBoxLayout(self)
		lay.addWidget(QLabel('Title:'))
		self.e_title = QLineEdit(str(pub.get('title') or ''))
		lay.addWidget(self.e_title)
		lay.addWidget(QLabel('Topic:'))
		self.e_topic = QLineEdit(str(pub.get('topic') or ''))
		lay.addWidget(self.e_topic)
		bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
		bb.accepted.connect(self.save)
		bb.rejected.connect(self.reject)
		lay.addWidget(bb)
	def save(self):
		r = api.update_pub(self.pub.get('id'), {'title': self.e_title.text(), 'topic': self.e_topic.text()})
		if r.get('ok'):
			self.accept()
		else:
			QMessageBox.warning(self, 'Loi', str(r)[:300])




class AIDialog(QDialog):
	def __init__(self, pub, parent=None):
		super().__init__(parent)
		self.pub = pub
		pid = pub.get('id')
		self.setWindowTitle('AI goi y #' + str(pid))
		self.resize(560, 500)
		lay = QVBoxLayout(self)
		self.sc = QLabel('Dang phan tich...')
		self.sc.setStyleSheet('font-size:14px;font-weight:700;color:#0A84FF')
		lay.addWidget(self.sc)
		lay.addWidget(QLabel('Tieu de goi y:'))
		self.tl = QPlainTextEdit()
		self.tl.setReadOnly(True)
		self.tl.setMaximumHeight(140)
		lay.addWidget(self.tl)
		lay.addWidget(QLabel('Tags goi y:'))
		self.tg = QPlainTextEdit()
		self.tg.setReadOnly(True)
		self.tg.setMaximumHeight(80)
		lay.addWidget(self.tg)
		use = QPushButton('Ap dung title dau tien')
		use.clicked.connect(self.apply)
		lay.addWidget(use)
		bb = QDialogButtonBox(QDialogButtonBox.Close)
		bb.rejected.connect(self.reject)
		lay.addWidget(bb)
		self.load(pid)
	def load(self, pid):
		r = api.ai_suggest(pid)
		s = api.ai_score(pid)
		if r.get('ok'):
			self.tl.setPlainText(chr(10).join(r.get('titles', [])))
			self.tg.setPlainText((chr(44) + chr(32)).join(r.get('tags', [])))
		if s.get('ok'):
			self.sc.setText('Score: ' + str(s.get('score')) + '/100 - ' + str(s.get('label')))
	def apply(self):
		txt = self.tl.toPlainText().split(chr(10))
		if not txt or not txt[0].strip():
			return
		pid = self.pub.get('id')
		r = api.update_pub(pid, {'title': txt[0].strip()})
		if r.get('ok'):
			QMessageBox.information(self, 'OK', 'Da ap dung title')
			self.accept()

class QueueCard(QFrame):
	def __init__(self, pub, oncheck, onview, onpublish, onschedule, onunschedule, onreject, onedit, onai, parent=None):
		super().__init__(parent)
		self.pub = pub
		self.oncheck = oncheck
		self.setObjectName('Card')
		self.setFixedWidth(220)
		lay = QVBoxLayout(self)
		lay.setContentsMargins(10, 10, 10, 10)
		lay.setSpacing(6)
		hdr = QHBoxLayout()
		self.cb = QCheckBox()
		self.cb.stateChanged.connect(lambda s: oncheck(pub, s == Qt.Checked))
		hdr.addWidget(self.cb)
		pid = pub.get('id')
		ttl = QLabel(str(pub.get('topic') or pub.get('title') or ('#' + str(pid))))
		ttl.setWordWrap(True)
		ttl.setStyleSheet('font-weight:700;font-size:12px')
		hdr.addWidget(ttl, 1)
		lay.addLayout(hdr)
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
		b1e = QPushButton('Sua')
		b1e.clicked.connect(lambda: onedit(pub))
		b1a = QPushButton('AI')
		b1a.clicked.connect(lambda: onai(pub))
		r1.addWidget(b1); r1.addWidget(b1e); r1.addWidget(b1a)
		lay.addLayout(r1)
		r2 = QHBoxLayout()
		b2 = QPushButton('Dang')
		b2.setObjectName('Primary')
		b2.clicked.connect(lambda: onpublish(pub))
		b3 = QPushButton('Lich')
		if sch:
			b3.setText('Huy')
			b3.clicked.connect(lambda: onunschedule(pub))
		else:
			b3.clicked.connect(lambda: onschedule(pub))
		r2.addWidget(b2); r2.addWidget(b3)
		lay.addLayout(r2)
		r3 = QHBoxLayout()
		b4 = QPushButton('Bo')
		b4.clicked.connect(lambda: onreject(pub))
		r3.addWidget(b4)
		lay.addLayout(r3)


class Queue(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.selected = set()
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
		self.btn_reload = QPushButton(i18n.t('btn.refresh'))
		self.btn_reload.clicked.connect(self.refresh)
		bar.addWidget(self.btn_reload)
		bar.addStretch()
		self.count = QLabel('')
		bar.addWidget(self.count)
		body.addLayout(bar)
		bar2 = QHBoxLayout()
		bar2.addWidget(QLabel('Da chon:'))
		self.selcount = QLabel('0')
		self.selcount.setStyleSheet('font-weight:700;color:#0A84FF')
		bar2.addWidget(self.selcount)
		bar2.addSpacing(12)
		self.btn_selall = QPushButton('Chon tat ca')
		self.btn_selall.clicked.connect(self.sel_all)
		bar2.addWidget(self.btn_selall)
		self.btn_clear = QPushButton('Bo chon')
		self.btn_clear.clicked.connect(self.sel_clear)
		bar2.addWidget(self.btn_clear)
		bar2.addSpacing(20)
		self.btn_bulkpub = QPushButton('Dang tat ca chon')
		self.btn_bulkpub.setObjectName('Primary')
		self.btn_bulkpub.clicked.connect(self.bulk_publish)
		bar2.addWidget(self.btn_bulkpub)
		self.btn_bulksch = QPushButton('Len lich tat ca chon')
		self.btn_bulksch.clicked.connect(self.bulk_schedule)
		bar2.addWidget(self.btn_bulksch)
		bar2.addStretch()
		body.addLayout(bar2)
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
		self.load_channels()
		self.refresh()

	def load_channels(self):
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

	def _updatesel(self):
		self.selcount.setText(str(len(self.selected)))

	def sel_all(self):
		for i in range(self.grid.count()):
			w = self.grid.itemAt(i).widget()
			if w and hasattr(w, 'cb'):
				w.cb.setChecked(True)

	def sel_clear(self):
		self.selected.clear()
		for i in range(self.grid.count()):
			w = self.grid.itemAt(i).widget()
			if w and hasattr(w, 'cb'):
				w.cb.setChecked(False)
		self._updatesel()

	def _oncheck(self, pub, checked):
		pid = pub.get('id')
		if checked:
			self.selected.add(pid)
		else:
			self.selected.discard(pid)
		self._updatesel()

	def refresh(self):
		self._clear()
		self.selected.clear()
		self._updatesel()
		ch = self.fch.currentData()
		st = self.fst.currentData()
		try:
			d = api.publications_queue(status=st, channel_id=ch)
		except Exception as e:
			self.count.setText('Loi: ' + str(e)); return
		items = d.get('items', [])
		self.count.setText(str(len(items)) + ' video')
		for i, pub in enumerate(items):
			card = QueueCard(pub, self._oncheck, self._view, self._publish, self._schedule, self._unschedule, self._reject, self._edit, self._ai)
			self.grid.addWidget(card, i // 5, i % 5)
		if not items:
			self.grid.addWidget(QLabel('Khong co video trong hang doi'), 0, 0)

	def _view(self, pub):
		VideoDialog(pub, self).exec()

	def _edit(self, pub):
		if EditDialog(pub, self).exec() == QDialog.Accepted:
			self.refresh()

	def _ai(self, pub):
		if AIDialog(pub, self).exec() == QDialog.Accepted:
			self.refresh()

	def _publish(self, pub):
		pid = pub.get('id')
		if QMessageBox.question(self, 'Dang', 'Dang video #' + str(pid) + '?') != QMessageBox.Yes: return
		r = api.publish_pub(pid)
		QMessageBox.information(self, 'Ket qua', str(r)[:400])
		self.refresh()

	def bulk_publish(self):
		ids = list(self.selected)
		if not ids:
			QMessageBox.information(self, 'Chon', 'Chua chon video nao'); return
		if QMessageBox.question(self, 'Dang', 'Dang ' + str(len(ids)) + ' video?') != QMessageBox.Yes: return
		r = api.bulk_publish(ids)
		QMessageBox.information(self, 'Ket qua', 'Da dang ' + str(r.get('count', 0)) + '/' + str(r.get('total', 0)))
		self.refresh()

	def bulk_schedule(self):
		ids = list(self.selected)
		if not ids:
			QMessageBox.information(self, 'Chon', 'Chua chon video nao'); return
		dlg = QDialog(self); dlg.setWindowTitle('Len lich ' + str(len(ids)) + ' video')
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
		r = api.bulk_schedule(ids, at)
		QMessageBox.information(self, 'Ket qua', 'Da len lich ' + str(r.get('count', 0)) + '/' + str(r.get('total', 0)))
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
