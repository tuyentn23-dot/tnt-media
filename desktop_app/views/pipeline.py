# -- coding: utf-8 --
# desktop_app/views/pipeline.py - Redesign v2 (topic + config grid + timeline + log + run)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
	QLineEdit, QComboBox, QDateTimeEdit, QPlainTextEdit, QMessageBox, QSizePolicy, QScrollArea, QFrame)
from PySide6.QtCore import Qt, QTimer, QDateTime
import i18n, api
from widgets_v2 import (Card, FieldGrid, CheckboxRow, Timeline, TimelineStep,
	PrimaryButton, SmallButton, RunButton, SecondaryButton)


STEPS = [
	{'num': '1', 'label': 'Phân tích', 'cat': 'analyze'},
	{'num': '2', 'label': 'Nội dung', 'cat': 'content'},
	{'num': '3', 'label': 'Dựng video', 'cat': 'render'},
	{'num': '4', 'label': 'Giọng nói', 'cat': 'voice'},
	{'num': '5', 'label': 'Đăng bài', 'cat': 'publish'},
]


class Pipeline(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._mod_meta = {}
		self._jid = None
		self._started = None
		self._lastn = -1
		self._lastchange = None
		self._build()
		try:
			self.sched_row.setVisible(False)
		except Exception:
			pass
		self._load_all()

	def _build(self):
		root = QVBoxLayout(self)
		root.setContentsMargins(20, 16, 12, 16)
		root.setSpacing(10)

		# === PIPELINE (TOP, header has inline run button) ===
		pipe_card = QFrame()
		pipe_card.setObjectName('Card')
		pipe_card.setStyleSheet("#Card{background:#FFFFFF;border:1px solid #E5E5EA;border-radius:12px}")
		pc_lay = QVBoxLayout(pipe_card)
		pc_lay.setContentsMargins(14, 10, 14, 10)
		pc_lay.setSpacing(8)
		# Header row: title + status + run button
		pc_hdr = QHBoxLayout()
		pc_hdr.setSpacing(8)
		pc_title = QLabel('PIPELINE · 5 BƯỚC')
		pc_title.setStyleSheet('font-size:10px;font-weight:700;color:#8E8E93;letter-spacing:0.8px')
		pc_hdr.addWidget(pc_title)
		pc_hdr.addStretch()
		self.lbl_status = QLabel('Sẵn sàng')
		self.lbl_status.setStyleSheet('font-size:11px;color:#8E8E93')
		pc_hdr.addWidget(self.lbl_status)
		self.btn_run = RunButton('▶ Chạy 2 video')
		self.btn_run.setMinimumHeight(30)
		self.btn_run.setMaximumHeight(30)
		self.btn_run.setMinimumWidth(140)
		self.btn_run.setMaximumWidth(180)
		self.btn_run.setStyleSheet('QPushButton{background:#0A84FF;color:white;border:none;border-radius:7px;padding:0 16px;font-size:12px;font-weight:600} QPushButton:hover{background:#0066CC} QPushButton:disabled{background:#B0D4FF}')
		pc_hdr.addWidget(self.btn_run)
		pc_lay.addLayout(pc_hdr)
		self.timeline = Timeline([(s['num'], s['label']) for s in STEPS])
		pc_lay.addWidget(self.timeline)
		mods_row = QHBoxLayout()
		mods_row.setSpacing(6)
		self.modules = []
		for s in STEPS:
			cb = QComboBox()
			cb.setMinimumContentsLength(6)
			cb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
			mods_row.addWidget(cb, 1)
			self.modules.append(cb)
		pc_lay.addLayout(mods_row)
		pipe_card.setMinimumHeight(175)
		root.addWidget(pipe_card)

		# === TOPIC ===
		topic_card = Card('Chủ đề video')
		topic_row = QHBoxLayout()
		topic_row.setSpacing(8)
		self.topic = QLineEdit()
		self.topic.setPlaceholderText('Nhập chủ đề hoặc để trống dùng AI gợi ý...')
		topic_row.addWidget(self.topic, 1)
		self.btn_trend = SecondaryButton('Trend')
		topic_row.addWidget(self.btn_trend)
		self.btn_viral = SecondaryButton('Viral')
		topic_row.addWidget(self.btn_viral)
		self.btn_adv = PrimaryButton('Gợi ý')
		topic_row.addWidget(self.btn_adv)
		topic_card.add(topic_row)
		topic_card.setMinimumHeight(75)
		root.addWidget(topic_card)

		# === CONFIG ===
		cfg_card = Card('Cấu hình')
		self.grid = FieldGrid(cols=4, vgap=6, hgap=8)
		self.ch = QComboBox()
		self.kind = QComboBox()
		self.length = QComboBox()
		self.length.addItem('Ngắn', None)
		self.length.addItem('Dài', 90)
		self.mode = QComboBox()
		self.mode.addItems(['Tự động', 'Duyệt trước'])
		self.when = QComboBox()
		self.when.addItems(['Đăng ngay', 'Hẹn lịch'])
		self.voice = QComboBox()
		self.preset = QComboBox()
		self.advisor_ideas = QComboBox()
		self.advisor_ideas.addItem('-- Chọn ý tưởng --', None)
		self.batch_count = QComboBox()
		for lbl, n in [('1 video', 1), ('2 video', 2), ('3 video', 3), ('5 video', 5), ('7 video', 7), ('10 video', 10)]:
			self.batch_count.addItem(lbl, n)
		self.batch_count.setCurrentIndex(1)
		self.sched = QDateTimeEdit()
		self.sched.setCalendarPopup(True)
		self.sched.setDateTime(QDateTime.currentDateTime().addSecs(3600))
		self.sched.setDisplayFormat('yyyy-MM-dd HH:mm')
		self.sched.setVisible(False)
		self._sched_hidden = True

		self.grid.add('Kênh', self.ch)
		self.grid.add('Loại nội dung', self.kind)
		self.grid.add('Độ dài', self.length)
		self.grid.add('Chế độ', self.mode)
		self.grid.add('Khi nào', self.when)
		self.sched_row = self.grid.add('Hẹn lịch', self.sched)
		self.grid.add('Giọng đọc', self.voice)
		self.grid.add('Sắc thái', self.preset)
		self.grid.add('Số lượng', self.batch_count)
		# Row 3: advisor (span 2) + checkbox row (span 2)
		adv_box = QWidget()
		adv_lay = QVBoxLayout(adv_box)
		adv_lay.setContentsMargins(0, 0, 0, 0)
		adv_lay.setSpacing(4)
		adv_lbl = QLabel('Ý tưởng (Advisor)')
		adv_lbl.setObjectName('FieldLabel')
		adv_lay.addWidget(adv_lbl)
		adv_lay.addWidget(self.advisor_ideas)
		self.grid.g.addWidget(adv_box, 2, 0, 1, 2)
		cfg_card.add(self.grid)

		chk_box = QWidget()
		chk_lay = QVBoxLayout(chk_box)
		chk_lay.setContentsMargins(0, 0, 0, 0)
		chk_lay.setSpacing(4)
		chk_lbl = QLabel('Tùy chọn')
		chk_lbl.setObjectName('FieldLabel')
		chk_lay.addWidget(chk_lbl)
		self.chk_row = CheckboxRow([
			('caption', 'Hiện caption', True),
			('music', 'Chỉ lồng nhạc', False),
		])
		chk_lay.addWidget(self.chk_row)
		self.grid.g.addWidget(chk_box, 2, 2, 1, 2)
		
		root.addWidget(cfg_card)

		# === LOG (expands) ===
		self.log = QPlainTextEdit()
		self.log.setReadOnly(True)
		self.log.setPlaceholderText('Nhật ký chạy sẽ hiện ở đây...')
		self.log.setMinimumHeight(50)
		root.addWidget(self.log, 1)

		# === SIGNALS ===
		self.ch.currentIndexChanged.connect(self.load_kinds)
		self.when.currentIndexChanged.connect(self._on_when_changed)
		self.batch_count.currentIndexChanged.connect(self._update_run_label)
		self.btn_trend.clicked.connect(self.do_trend)
		self.btn_viral.clicked.connect(self.do_viral)
		self.btn_adv.clicked.connect(self.load_advisor)
		self.advisor_ideas.currentIndexChanged.connect(self._apply_idea)
		self.btn_run.clicked.connect(self.do_run)

	def _on_when_changed(self, idx):
		show = (idx == 1)
		self.sched.setVisible(show)
		try:
			self.sched_row.setVisible(show)
		except Exception:
			pass

	def _update_run_label(self):
		n = int(self.batch_count.currentData() or 1)
		self.btn_run.setText('Chạy ' + str(n) + ' video')

	def _load_all(self):
		try:
			self.load_channels()
		except Exception as e:
			self.logline('! Load channels loi: ' + str(e)[:100])
		try:
			self.load_voice_presets()
		except Exception as e:
			self.logline('! Load voice loi: ' + str(e)[:100])
		try:
			self.load_modules()
		except Exception as e:
			self.logline('! Load modules loi: ' + str(e)[:100])
		self._update_run_label()

	def logline(self, txt):
		self.log.appendPlainText(str(txt))
		sb = self.log.verticalScrollBar()
		sb.setValue(sb.maximum())

	def load_channels(self):
		d = api.channels()
		items = d.get('channels', d.get('items', d if isinstance(d, list) else []))
		self.ch.blockSignals(True)
		self.ch.clear()
		if not items:
			self.ch.addItem('Chua co kenh', None)
		for it in items:
			if isinstance(it, dict):
				nm = str(it.get('name', it.get('id')))
				iid = it.get('id')
			else:
				nm = str(it)
				iid = it
			self.ch.addItem(nm, iid)
		self.ch.blockSignals(False)
		self.load_kinds()

	def load_kinds(self):
		cid = self.ch.currentData()
		self.kind.clear()
		if not cid:
			self.kind.addItem('(chua chon kenh)', None)
			return
		try:
			d = api.get('/api/config/kinds?channel_id=' + str(cid))
			items = d.get('items', [])
		except Exception:
			items = []
		if not items:
			self.kind.addItem('(khong co kind)', None)
		for k in items:
			self.kind.addItem(str(k), str(k))

	def load_modules(self):
		d = api.modules()
		items = d.get('items', d if isinstance(d, list) else [])
		by = {}
		meta = {}
		for it in items:
			if not isinstance(it, dict):
				continue
			cat = it.get('category', 'other')
			name = it.get('name', '?')
			ver = it.get('version', '')
			label = name + ' v' + str(ver)
			by.setdefault(cat, []).append(label)
			meta[label] = it
		self._mod_meta = meta
		for i, s in enumerate(STEPS):
			cb = self.modules[i]
			cb.clear()
			cb.addItem('-- ' + s['label'] + ' --', None)
			for lbl in by.get(s['cat'], []):
				cb.addItem(lbl, lbl)

	def load_voice_presets(self):
		try:
			v = api.voices().get('items', [])
		except Exception:
			v = []
		self.voice.clear()
		for it in v:
			if isinstance(it, dict):
				self.voice.addItem(str(it.get('label', it.get('id'))), it.get('id'))
			else:
				self.voice.addItem(str(it), str(it))
		if self.voice.count() == 0:
			self.voice.addItem('female_north', 'female_north')
		try:
			pz = api.presets().get('items', [])
		except Exception:
			pz = []
		self.preset.clear()
		for it in pz:
			if isinstance(it, dict):
				self.preset.addItem(str(it.get('label', it.get('id'))), it.get('id'))
			else:
				self.preset.addItem(str(it), str(it))
		if self.preset.count() == 0:
			self.preset.addItem('default', 'default')

	def do_trend(self):
		self.logline('> Đang thu thập xu hướng...')
		try:
			niche = (self.kind.currentData() or self.kind.currentText() or '').strip().lower()
			rc = api.post('/api/trends/collect', {'niche': niche, 'limit': 30})
			self.logline(' Thu thap: ' + str(rc.get('collected', 0)) + ' / luu: ' + str(rc.get('saved', 0)))
		except Exception as e:
			self.logline(' Loi: ' + str(e)[:120])

	def do_viral(self):
		self.logline('> Đang phân tích viral...')
		kw = self.topic.text().strip() or (self.kind.currentText() if self.kind.count() else 'meo con')
		try:
			r = api.post('/api/viral/search', {'query': kw, 'max_results': 15})
			if not r.get('ok'):
				self.logline(' Loi: ' + str(r.get('error'))[:120])
				return
			items = r.get('items', [])
			self.logline(' Tim thay: ' + str(len(items)) + ' video')
		except Exception as e:
			self.logline(' Loi: ' + str(e)[:120])

	def load_advisor(self):
		self.logline('> Lấy gợi ý từ Advisor...')
		try:
			url = '/api/studio/advice?force=0'
			cid = self.ch.currentData()
			if cid:
				url += '&channel_id=' + str(cid)
			kid = self.kind.currentData()
			if kid:
				url += '&kind=' + str(kid)
			d = api.get(url)
			adv = (d or {}).get('advisor') or {}
			self.advisor_ideas.blockSignals(True)
			self.advisor_ideas.clear()
			self.advisor_ideas.addItem('-- Chọn ý tưởng --', None)
			for idea in (adv.get('next_ideas') or []):
				ttl = (idea.get('title') or '')[:80]
				if ttl:
					self.advisor_ideas.addItem(ttl, ttl)
			self.advisor_ideas.blockSignals(False)
			self.logline(' Advisor OK: ' + str(len(adv.get('next_ideas') or [])) + ' y tuong')
		except Exception as e:
			self.logline('! Advisor loi: ' + str(e)[:120])

	def _apply_idea(self, idx):
		t = self.advisor_ideas.currentData()
		if t:
			self.topic.setText(t)
			self.logline('> Áp dụng: ' + t[:60])
	def do_run(self):
		cid = self.ch.currentData()
		if cid is None:
			self.logline('! Chưa chọn kênh')
			return
		n = int(self.batch_count.currentData() or 1)
		body = {
			'channel_id': cid,
			'count': n,
			'topic': self.topic.text(),
			'require_approval': (self.mode.currentIndex() == 1),
			'voice_override': self.voice.currentData(),
			'voice_preset': self.preset.currentData(),
			}
		k = self.kind.currentData()
		if k:
			body['kind'] = k
		lo = self.length.currentData()
		if lo:
			body['length_override'] = lo
		mods = {}
		for i, cb in enumerate(self.modules):
			cur = cb.currentData()
			if cur:
				mods[STEPS[i]['cat']] = cur
		mods['_opts'] = {'caption': self.chk_row.is_checked('caption'), 'music_only': self.chk_row.is_checked('music')}
		body['modules'] = mods
		if self.when.currentIndex() == 1:
			body['run_at'] = self.sched.dateTime().toString('yyyy-MM-dd HH:mm:ss')
		self.logline('> Tao job: kenh=' + str(cid) + ', so luong=' + str(n))
		try:
			r = api.create_job(body)
		except Exception as e:
			self.logline('! Lỗi API: ' + str(e)[:150])
			return
		jid = r.get('job_id', r.get('id'))
		if not jid:
			self.logline('! Không tạo được job: ' + str(r)[:150])
			return
		self.logline('> Dang chay: ' + str(jid))
		try:
			rr = api.run_job(jid)
		except Exception as e:
			self.logline('! Lỗi chạy: ' + str(e)[:150])
			return
		if rr.get('ok') is False:
			self.logline('! Run loi: ' + str(rr)[:150])
			self._set_timeline_error()
			return
		self._jid = jid
		import time as _tm
		self._started = _tm.time()
		self._lastn = -1
		self._lastchange = _tm.time()
		self.btn_run.setEnabled(False)
		self.lbl_status.setText('Đang chạy ' + str(n) + ' video...')
		self.timeline.set_state(0, TimelineStep.STATE_RUNNING)
		if not hasattr(self, "timer"):
			self.timer = QTimer(self)
			self.timer.timeout.connect(self.poll_job)
		self.timer.start(1000)

	def _set_timeline_error(self):
		self.timeline.set_state(0, TimelineStep.STATE_ERROR)
		self.lbl_status.setText('Loi - kiem tra nhat ky' )
		self.btn_run.setEnabled(True)

	def poll_job(self):
		jid = self._jid
		if not jid:
			return
		import time, sqlite3
		try:
			d = api.job_detail(jid)
		except Exception:
			return
		if not isinstance(d, dict):
			return
		tail = d.get('log_tail', [])
		if tail:
			self.log.setPlainText(chr(10).join(tail))
			sb = self.log.verticalScrollBar()
			sb.setValue(sb.maximum())
		st = str(d.get('status') or '')
		try:
			cc = sqlite3.connect("state/pipeline.db")
			row = cc.execute('SELECT COUNT() FROM publications WHERE job_id=?', (jid,)).fetchone()
			n = int(row[0]) if row else 0
			cc.close()
		except Exception:
			n = 0
		total = int(d.get('count') or 1)
		running = bool(d.get('running'))
		if not self._started:
			self._started = time.time()
		el = int(time.time() - self._started)
		mins = el // 60
		secs = el % 60
		tstr = ((str(mins) + 'm ') if mins else '') + str(secs) + 's'
		if n != self._lastn:
			self._lastn = n
			self._lastchange = time.time()
		if st in ('done', 'completed', 'success'):
			self.timer.stop()
			self.timeline.set_state(5, TimelineStep.STATE_DONE)
			self.lbl_status.setText('Hoàn tất ' + str(n) + ' video / ' + tstr)
			self.btn_run.setEnabled(True)
			self.logline('> Xong ' + str(n) + ' video sau ' + tstr)
		elif st in ('error', 'failed'):
			self.timer.stop()
			self._set_timeline_error()
		elif running or st in ("running", "pending", "queued"):
			step = min(4, n)
			self.timeline.set_state(step, TimelineStep.STATE_RUNNING)
			msg = 'Chạy ' + tstr + ' - ' + str(n) + '/' + str(total)
			self.lbl_status.setText(msg)