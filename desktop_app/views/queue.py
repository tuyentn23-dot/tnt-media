# -- coding: utf-8 --
# desktop_app/views/queue.py - Redesign v2: list view + floating bulk
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
	QPushButton, QScrollArea, QFrame, QDialog, QDialogButtonBox,
	QDateTimeEdit, QMessageBox, QLineEdit, QPlainTextEdit, QCheckBox)
from PySide6.QtCore import Qt, QDateTime, QUrl
from PySide6.QtGui import QPixmap
try:
	from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
	from PySide6.QtMultimediaWidgets import QVideoWidget
	HAS_MULTI = True
except Exception:
	HAS_MULTI = False
import i18n, api
from widgets import busy_wrap
from widgets_v2 import (StatusBadge, QueueRow, SmallButton, PrimaryButton,
	DangerButton, EmptyState)


def _friendly_publish_result(r):
	if not isinstance(r, dict):
		return False, 'Loi', str(r)[:200]
	if r.get('ok'):
		yid = r.get('youtube_id') or ''
		url = r.get('url') or (('https://youtu.be/' + yid) if yid else '')
		msg = 'Da dang len YouTube thanh cong.'
		if url:
			msg += '\n' + url
		return True, 'Dang thanh cong', msg
	err = str(r.get('error') or r.get('reason') or 'Dang that bai')
	low = err.lower()
	if 'quality' in low or 'gate' in low or 'score' in low:
		err = 'Video chua dat chat luong toi thieu (quality gate).'
	elif 'token' in low or 'auth' in low or 'credential' in low:
		err = 'Loi xac thuc YouTube (token het han?).'
	elif 'timeout' in low or 'network' in low or 'connect' in low:
		err = 'Loi mang khi tai len.'
	return False, 'Dang that bai', err[:400]


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
		bb = QDialogButtonBox(QDialogButtonBox.Close)
		bb.rejected.connect(self.reject)
		lay.addWidget(bb)


class EditDialog(QDialog):
	def __init__(self, pub, parent=None):
		super().__init__(parent)
		self.pub = pub
		self.setWindowTitle('Sua metadata #' + str(pub.get('id')))
		self.resize(520, 420)
		lay = QVBoxLayout(self)
		lay.addWidget(QLabel('Tieu de:'))
		self.e_title = QLineEdit(str(pub.get('title') or ''))
		lay.addWidget(self.e_title)
		lay.addWidget(QLabel('Chu de:'))
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
		use = QPushButton('Ap dung tieu de dau tien')
		use.clicked.connect(self.apply)
		lay.addWidget(use)
		bb = QDialogButtonBox(QDialogButtonBox.Close)
		bb.rejected.connect(self.reject)
		lay.addWidget(bb)
		self._load(pid)

	def _load(self, pid):
		r = api.ai_suggest(pid)
		s = api.ai_score(pid)
		if r.get('ok'):
			self.tl.setPlainText(chr(10).join(r.get('titles', [])))
			self.tg.setPlainText(', '.join(r.get('tags', [])))
		if s.get('ok'):
			self.sc.setText('Score: ' + str(s.get('score')) + '/100 - ' + str(s.get('label')))

	def apply(self):
		txt = self.tl.toPlainText().split(chr(10))
		if not txt or not txt[0].strip():
			return
		pid = self.pub.get('id')
		r = api.update_pub(pid, {'title': txt[0].strip()})
		if r.get('ok'):
			QMessageBox.information(self, 'OK', 'Da ap dung tieu de')
			self.accept()


class Queue(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.selected = set()
		self._rows = []
		self._build()
		self._load_channels()
		self.refresh()

	def _build(self):
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)

		# Filter row
		filt = QWidget()
		filt.setObjectName("FilterBar")
		filt.setStyleSheet("#FilterBar{background:white;border-bottom:1px solid #E5E5EA}")
		fh = QHBoxLayout(filt)
		fh.setContentsMargins(16, 10, 16, 10)
		fh.setSpacing(8)
		fh.addWidget(QLabel('Kênh:'))
		self.fch = QComboBox()
		self.fch.addItem('Tất cả', None)
		fh.addWidget(self.fch, 1)
		fh.addWidget(QLabel('Trạng thái:'))
		self.fst = QComboBox()
		self.fst.addItem('Chưa đăng', 'rendered')
		self.fst.addItem('Đã hẹn', 'scheduled')
		self.fst.addItem('Đã đăng', 'published')
		self.fst.addItem('Đã gỡ', 'verify_failed')
		self.fst.addItem('Tất cả', None)
		self.fst.setMinimumContentsLength(8)
		self.fst.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
		fh.addWidget(self.fst, 1)
		self.count = QLabel("")
		self.count.setStyleSheet("font-size:10px;color:#8E8E93")
		fh.addWidget(self.count)
		root.addWidget(filt)

		# Toolbar (select)
		tb = QWidget()
		tb.setObjectName("Toolbar")
		tb.setStyleSheet("#Toolbar{background:white;border-bottom:1px solid #E5E5EA}")
		th = QHBoxLayout(tb)
		th.setContentsMargins(16, 8, 16, 8)
		th.setSpacing(6)
		th.addWidget(QLabel('Đã chọn:'))
		self.selcount = QLabel("0")
		self.selcount.setStyleSheet("font-weight:700;color:#0A84FF")
		th.addWidget(self.selcount)
		th.addStretch()
		self.btn_selall = SmallButton('Chọn tất cả')
		self.btn_selall.clicked.connect(self.sel_all)
		th.addWidget(self.btn_selall)
		self.btn_clear = SmallButton('Bỏ chọn')
		self.btn_clear.clicked.connect(self.sel_clear)
		th.addWidget(self.btn_clear)
		self.btn_reload = SmallButton('Làm mới')
		self.btn_reload.clicked.connect(self.refresh)
		th.addWidget(self.btn_reload)
		root.addWidget(tb)

		# Scroll list
		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)
		self.scroll.setFrameShape(QFrame.NoFrame)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.container = QWidget()
		self.list_lay = QVBoxLayout(self.container)
		self.list_lay.setContentsMargins(12, 12, 12, 12)
		self.list_lay.setSpacing(8)
		self.list_lay.addStretch()
		self.scroll.setWidget(self.container)
		root.addWidget(self.scroll, 1)

		# Empty state (hidden by default)
		self.empty = EmptyState(chr(128230), "Chua co video trong hang doi", "Tao video dau tien o tab Studio")
		self.empty.setVisible(False)
		root.addWidget(self.empty, 1)

		# Bulk action bar (always visible)
		bulk = QWidget()
		bulk.setObjectName("BulkBar")
		bulk.setStyleSheet("#BulkBar{background:white;border-top:1px solid #E5E5EA}")
		bh = QHBoxLayout(bulk)
		bh.setContentsMargins(16, 10, 16, 10)
		bh.setSpacing(6)
		self.btn_bulkpub = PrimaryButton('Đăng chọn')
		self.btn_bulkpub.setObjectName("SmallButtonPrimary")
		self.btn_bulkpub.clicked.connect(self.bulk_publish)
		bh.addWidget(self.btn_bulkpub, 1)
		self.btn_bulksch = SmallButton('Lên lịch')
		self.btn_bulksch.clicked.connect(self.bulk_schedule)
		bh.addWidget(self.btn_bulksch, 1)
		self.btn_autosch = SmallButton('Tối ưu')
		self.btn_autosch.setObjectName("SmallButtonPrimary")
		self.btn_autosch.clicked.connect(self.auto_schedule)
		bh.addWidget(self.btn_autosch, 1)
		self.btn_bulkrej = DangerButton('Loại bỏ')
		self.btn_bulkrej.setObjectName("SmallButtonDanger")
		self.btn_bulkrej.clicked.connect(self.bulk_reject)
		bh.addWidget(self.btn_bulkrej, 1)
		root.addWidget(bulk)

		self.fch.currentIndexChanged.connect(self.refresh)
		self.fst.currentIndexChanged.connect(self.refresh)

	def _load_channels(self):
		try:
			d = api.channels()
			items = d.get('channels', d.get('items', []))
		except Exception:
			items = []
		for it in items:
			if isinstance(it, dict):
				self.fch.addItem(str(it.get('id')), it.get('id'))
	def refresh(self):
		for r in self._rows:
			r.setParent(None)
			r.deleteLater()
		self._rows = []
		self.selected = set()
		self._updatesel()
		ch = self.fch.currentData()
		st = self.fst.currentData()
		try:
			d = api.publications_queue(status=st, channel_id=ch)
		except Exception as e:
			self.count.setText("Loi: " + str(e)[:40])
			return
		items = d.get("items", [])
		self.count.setText(str(len(items)) + " video")
		if not items:
			self.scroll.setVisible(False)
			self.empty.setVisible(True)
			return
		self.scroll.setVisible(True)
		self.empty.setVisible(False)
		for pub in items:
			row = QueueRow(pub)
			row.clicked.connect(self._on_row_click)
			row.toggled.connect(self._on_toggle)
			row.menu_clicked.connect(self._on_menu)
			self.list_lay.insertWidget(self.list_lay.count() - 1, row)
			self._rows.append(row)

	def _on_row_click(self, pub):
		try:
			VideoDialog(pub, self).exec()
		except Exception as e:
			print('[queue] video dialog error:', e)

	def _on_toggle(self, pub, checked):
		pid = pub.get("id")
		if checked:
			self.selected.add(pid)
		else:
			self.selected.discard(pid)
		self._updatesel()

	def _on_menu(self, pub):
		from PySide6.QtWidgets import QMenu
		m = QMenu(self)
		m.addAction("Xem", lambda: self._view(pub))
		m.addAction("Sua", lambda: self._edit(pub))
		m.addAction("AI goi y", lambda: self._ai(pub))
		m.addSeparator()
		m.addAction("Dang", lambda: self._publish(pub))
		m.addAction("Len lich", lambda: self._schedule(pub))
		m.addAction("Loai bo", lambda: self._reject(pub))
		m.exec_(self.cursor().pos())

	def _updatesel(self):
		self.selcount.setText(str(len(self.selected)))

	def sel_all(self):
		for r in self._rows:
			r.set_checked(True)

	def sel_clear(self):
		for r in self._rows:
			r.set_checked(False)
		self.selected.clear()
		self._updatesel()

	def _selected_ids(self):
		return list(self.selected)

	def _view(self, pub):
		VideoDialog(pub, self).exec()

	def _edit(self, pub):
		if EditDialog(pub, self).exec() == QDialog.Accepted:
			self.refresh()

	def _ai(self, pub):
		if AIDialog(pub, self).exec() == QDialog.Accepted:
			self.refresh()

	def _publish(self, pub):
		pid = pub.get("id")
		if QMessageBox.question(self, "Dang", "Dang video #" + str(pid) + "?") != QMessageBox.Yes:
			return
		r = busy_wrap(self, lambda: api.publish_pub(pid), "Dang dang...")
		ok, ttl, body = _friendly_publish_result(r)
		if ok:
			QMessageBox.information(self, ttl, body)
		else:
			QMessageBox.warning(self, ttl, body)
		self.refresh()

	def bulk_publish(self):
		ids = self._selected_ids()
		if not ids:
			QMessageBox.information(self, "Chon", "Chua chon video nao")
			return
		if QMessageBox.question(self, "Dang", "Dang " + str(len(ids)) + " video?") != QMessageBox.Yes:
			return
		r = busy_wrap(self, lambda: api.bulk_publish(ids), "Dang dang " + str(len(ids)) + " video...")
		cnt = r.get("count", 0)
		tot = r.get("total", 0)
		if cnt == tot and tot > 0:
			QMessageBox.information(self, "OK", "Da dang " + str(cnt) + "/" + str(tot))
		elif cnt > 0:
			QMessageBox.warning(self, "Mot phan", "Da dang " + str(cnt) + "/" + str(tot))
		else:
			QMessageBox.warning(self, "That bai", "Khong dang duoc video nao")
		self.refresh()

	def bulk_schedule(self):
		ids = self._selected_ids()
		if not ids:
			QMessageBox.information(self, "Chon", "Chua chon video nao")
			return
		dlg = QDialog(self)
		dlg.setWindowTitle("Len lich " + str(len(ids)) + " video")
		v = QVBoxLayout(dlg)
		v.addWidget(QLabel("Chon thoi gian:"))
		de = QDateTimeEdit(QDateTime.currentDateTime().addSecs(3600))
		de.setCalendarPopup(True)
		de.setDisplayFormat('yyyy-MM-dd HH:mm')
		v.addWidget(de)
		bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		bb.accepted.connect(dlg.accept)
		bb.rejected.connect(dlg.reject)
		v.addWidget(bb)
		if dlg.exec() != QDialog.Accepted:
			return
		at = de.dateTime().toString('yyyy-MM-dd HH:mm')
		r = busy_wrap(self, lambda: api.bulk_schedule(ids, at), "Dang len lich...")
		QMessageBox.information(self, "KQ", "Da len " + str(r.get("count", 0)) + "/" + str(r.get("total", 0)))
		self.refresh()

	def auto_schedule(self):
		ids = self._selected_ids()
		ch = self.fch.currentData()
		if ids:
			msg = "Toi uu lich cho " + str(len(ids)) + " video da chon?"
		else:
			msg = "Toi uu lich cho TAT CA video chua dang?"
		if QMessageBox.question(self, "Toi uu", msg) != QMessageBox.Yes:
			return
		r = busy_wrap(self, lambda: api.auto_schedule(ids if ids else None, ch, 2), "Dang len...")
		if not isinstance(r, dict) or not r.get("ok"):
			QMessageBox.warning(self, "Loi", str(r)[:300])
			return
		QMessageBox.information(self, "OK", "Da len " + str(r.get("count", 0)) + "/" + str(r.get("total", 0)))
		self.refresh()

	def bulk_reject(self):
		ids = self._selected_ids()
		if not ids:
			QMessageBox.information(self, "Chon", "Chua chon video nao")
			return
		if QMessageBox.question(self, "Loai", "Loai bo " + str(len(ids)) + " video?") != QMessageBox.Yes:
			return
		ok = 0
		for pid in ids:
			try:
				api.reject(pid)
				ok += 1
			except Exception:
				pass
		QMessageBox.information(self, "KQ", "Da loai " + str(ok) + "/" + str(len(ids)))
		self.refresh()

	def _schedule(self, pub):
		pid = pub.get("id")
		dlg = QDialog(self)
		dlg.setWindowTitle("Len lich #" + str(pid))
		v = QVBoxLayout(dlg)
		v.addWidget(QLabel("Chon thoi gian:"))
		de = QDateTimeEdit(QDateTime.currentDateTime().addSecs(3600))
		de.setCalendarPopup(True)
		de.setDisplayFormat('yyyy-MM-dd HH:mm')
		v.addWidget(de)
		bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		bb.accepted.connect(dlg.accept)
		bb.rejected.connect(dlg.reject)
		v.addWidget(bb)
		if dlg.exec() != QDialog.Accepted:
			return
		at = de.dateTime().toString('yyyy-MM-dd HH:mm')
		r = api.schedule_pub(pid, at)
		QMessageBox.information(self, "KQ", str(r)[:300])
		self.refresh()

	def _reject(self, pub):
		pid = pub.get("id")
		if QMessageBox.question(self, "Loai", "Loai video #" + str(pid) + "?") != QMessageBox.Yes:
			return
		api.reject(pid)
		self.refresh()