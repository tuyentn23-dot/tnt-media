# -- coding: utf-8 --
# desktop_app/views/pipeline.py - Redesign v2 (topic + config grid + timeline + log + run)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
	QLineEdit, QComboBox, QDateTimeEdit, QPlainTextEdit, QMessageBox, QSizePolicy, QScrollArea, QFrame, QDialog, QDialogButtonBox, QCheckBox)
from PySide6.QtCore import Qt, QTimer, QDateTime
import i18n, api
from widgets_v2 import (Card, FieldGrid, FieldRow, CheckboxRow, Timeline, TimelineStep,
	PrimaryButton, SmallButton, RunButton, SecondaryButton)


STEPS = [
	{'num': '1', 'label': 'Phân tích', 'cat': 'analyze'},
	{'num': '2', 'label': 'Nội dung', 'cat': 'content'},
	{'num': '3', 'label': 'Dựng video', 'cat': 'render'},
	{'num': '4', 'label': 'Giọng nói', 'cat': 'voice'},
	{'num': '5', 'label': 'Đăng bài', 'cat': 'publish'},
]


class SuggestDialog(QDialog):
	def __init__(self, title, items, on_pick, parent=None, on_multi=None):
		super().__init__(parent)
		self.setWindowTitle(title)
		self.resize(700, 540)
		self._items = items
		self._on_pick = on_pick
		self._on_multi = on_multi
		self._checkboxes = []
		lay = QVBoxLayout(self)
		lay.setContentsMargins(16, 14, 16, 14)
		lay.setSpacing(8)
		hdr = QLabel(title)
		hdr.setStyleSheet('font-size:14px;font-weight:700')
		lay.addWidget(hdr)
		if on_multi:
			hint_txt = 'Tick nhiều ý tưởng để tạo nhiều video riêng, hoặc bấm "Dùng" để chọn 1'
		else:
			hint_txt = 'Chọn một mục để điền vào ô chủ đề'
		hint = QLabel(hint_txt)
		hint.setStyleSheet('font-size:11px;color:#8E8E93')
		lay.addWidget(hint)
		if not items:
			empty = QLabel('Không có kết quả')
			empty.setStyleSheet('color:#8E8E93;padding:40px')
			empty.setAlignment(Qt.AlignCenter)
			lay.addWidget(empty)
		else:
			scroll = QScrollArea()
			scroll.setWidgetResizable(True)
			scroll.setFrameShape(QFrame.NoFrame)
			box = QWidget()
			bl = QVBoxLayout(box)
			bl.setContentsMargins(0, 0, 0, 0)
			bl.setSpacing(6)
			for idx, it in enumerate(items):
				row = QFrame()
				row.setObjectName('Card')
				row.setStyleSheet('#Card{background:#FFFFFF;border:1px solid #E5E5EA;border-radius:8px}')
				rh = QHBoxLayout(row)
				rh.setContentsMargins(10, 8, 10, 8)
				rh.setSpacing(8)
				if on_multi:
					cb = QCheckBox()
					self._checkboxes.append(cb)
					rh.addWidget(cb)
				col = QVBoxLayout()
				col.setSpacing(2)
				ttl = QLabel(str(it.get('title') or '')[:120])
				ttl.setStyleSheet('font-size:12px;font-weight:600')
				ttl.setWordWrap(True)
				col.addWidget(ttl)
				sub = it.get('subtitle') or ''
				if sub:
					sub_lbl = QLabel(str(sub)[:120])
					sub_lbl.setStyleSheet('font-size:10px;color:#8E8E93')
					col.addWidget(sub_lbl)
				rh.addLayout(col, 1)
				btn = PrimaryButton('Dùng')
				btn.setMinimumWidth(70)
				btn.clicked.connect(lambda _=False, x=idx: self._pick(x))
				rh.addWidget(btn)
				bl.addWidget(row)
			bl.addStretch()
			scroll.setWidget(box)
			lay.addWidget(scroll, 1)
		if on_multi:
			rowb = QHBoxLayout()
			rowb.addStretch()
			self.btn_multi = PrimaryButton('Áp dụng đã tick')
			self.btn_multi.setMinimumWidth(160)
			self.btn_multi.clicked.connect(self._apply_multi)
			rowb.addWidget(self.btn_multi)
			lay.addLayout(rowb)
		bb = QDialogButtonBox(QDialogButtonBox.Close)
		bb.rejected.connect(self.reject)
		lay.addWidget(bb)

	def _pick(self, idx):
		try:
			it = self._items[idx]
		except Exception:
			return
		if self._on_pick:
			self._on_pick(it)
		self.accept()

	def _apply_multi(self):
		picked = [self._items[i] for i, cb in enumerate(self._checkboxes) if cb.isChecked()]
		if not picked:
			return
		if self._on_multi:
			self._on_multi(picked)
		self.accept()


class Pipeline(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._mod_meta = {}
		self._jid = None
		self._started = None
		self._lastn = -1
		self._lastchange = None
		self.multi_topics = []
		self.multi_topic_box = None
		self.multi_topic_lay = None
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
		self.multi_topic_box = QWidget()
		self.multi_topic_lay = QVBoxLayout(self.multi_topic_box)
		self.multi_topic_lay.setContentsMargins(0, 6, 0, 0)
		self.multi_topic_lay.setSpacing(3)
		self.multi_topic_box.setVisible(False)
		topic_card.add(self.multi_topic_box)
		topic_card.setMinimumHeight(75)
		root.addWidget(topic_card)

		# === CONFIG ===
		cfg_card = Card('Cấu hình')
		self.grid = FieldGrid(cols=4, vgap=6, hgap=10)
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
		self.grid.add('Giọng đọc', self.voice)
		self.grid.add('Sắc thái', self.preset)
		self.grid.add('Số lượng', self.batch_count)
		self.sched_row = FieldRow('Hẹn lịch', self.sched)
		self.sched_row.setVisible(False)
		cfg_card.add(self.sched_row)
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
		self.btn_run.setText('▶ Chạy ' + str(n) + ' video')

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
		self.btn_trend.setEnabled(False)
		self.btn_trend.setText('Đang tải...')
		try:
			niche = (self.kind.currentData() or self.kind.currentText() or '').strip().lower()
			rc = api.post('/api/trends/collect', {'niche': niche, 'limit': 30})
			self.logline(' Thu thập: ' + str(rc.get('collected', 0)) + ' / lưu: ' + str(rc.get('saved', 0)))
			items = rc.get('items', [])
			if not items:
				self.logline(' Không có xu hướng mới')
			else:
				suggestions = []
				for it in items:
					ttl = str(it.get('title') or '')
					if not ttl:
						continue
					views = it.get('views', 0)
					src = str(it.get('source') or '')
					sub = f'{views:,} views - {src}' if views else src
					suggestions.append({'title': ttl, 'subtitle': sub})
				self._show_suggestions(
					'Xu hướng: ' + str(len(suggestions)) + ' từ YouTube',
					suggestions)
		except Exception as e:
			self.logline(' Lỗi: ' + str(e)[:120])
		finally:
			self.btn_trend.setEnabled(True)
			self.btn_trend.setText('Trend')

	def do_viral(self):
		self.logline('> Đang phân tích viral...')
		self.btn_viral.setEnabled(False)
		self.btn_viral.setText('Đang tải...')
		kw = self.topic.text().strip() or (self.kind.currentText() if self.kind.count() else '')
		if not kw:
			self.logline('! Nhập chủ đề hoặc chọn loại nội dung trước')
			self.btn_viral.setEnabled(True)
			self.btn_viral.setText('Viral')
			return
		try:
			r = api.post('/api/viral/search', {'query': kw, 'max_results': 15})
			if not r.get('ok'):
				self.logline(' Lỗi: ' + str(r.get('error'))[:120])
				return
			items = r.get('items', [])
			self.logline(' Tìm thấy: ' + str(len(items)) + ' video viral')
			suggestions = []
			for it in items:
				ttl = str(it.get('title') or '')
				if not ttl:
					continue
				views = it.get('views', 0)
				ch = str(it.get('channel') or '')
				dur = it.get('duration_s', 0)
				parts = [ch]
				if views: parts.append(f'{views:,} views')
				if dur: parts.append(f'{dur}s')
				suggestions.append({'title': ttl, 'subtitle': ' - '.join(parts)})
			self._show_suggestions(
				f'Viral: {len(suggestions)} video từ khóa "{kw}"',
				suggestions)
		except Exception as e:
			self.logline(' Lỗi: ' + str(e)[:120])
		finally:
			self.btn_viral.setEnabled(True)
			self.btn_viral.setText('Viral')

	def load_advisor(self):
		self.logline('> Lấy gợi ý từ Advisor (có thể mất 20-30s)...')
		self.btn_adv.setEnabled(False)
		self.btn_adv.setText('Đang phân tích...')
		try:
			url = '/api/studio/advice?force=1'
			cid = self.ch.currentData()
			if cid:
				url += '&channel_id=' + str(cid)
			kid = self.kind.currentData()
			if kid:
				url += '&kind=' + str(kid)
			d = api.get(url, timeout=90)
			adv = (d or {}).get('advisor') or {}
			ideas = adv.get('next_ideas') or []
			suggestions = []
			for idea in ideas:
				ttl = str(idea.get('title') or '')[:100]
				if not ttl:
					continue
				reason = str(idea.get('reason') or idea.get('why') or '')[:100]
				suggestions.append({'title': ttl, 'subtitle': reason})
			# also fill dropdown
			self.advisor_ideas.blockSignals(True)
			self.advisor_ideas.clear()
			self.advisor_ideas.addItem('-- Chọn ý tưởng --', None)
			for s in suggestions:
				self.advisor_ideas.addItem(s['title'][:80], s['title'])
			self.advisor_ideas.blockSignals(False)
			self.logline(' Advisor: ' + str(len(suggestions)) + ' ý tưởng')
			if suggestions:
				self._show_suggestions(
					f'Advisor: {len(suggestions)} ý tưởng gợi ý',
					suggestions)
			else:
				self.logline('! Advisor không trả về ý tưởng nào')
		except Exception as e:
			self.logline('! Lỗi Advisor: ' + str(e)[:120])
		finally:
			self.btn_adv.setEnabled(True)
			self.btn_adv.setText('Gợi ý')

	def _render_multi_topics(self):
		if self.multi_topic_lay is None:
			return
		while self.multi_topic_lay.count():
			w = self.multi_topic_lay.takeAt(0).widget()
			if w:
				w.deleteLater()
		if not self.multi_topics:
			self.multi_topic_box.setVisible(False)
			return
		self.multi_topic_box.setVisible(True)
		n = int(self.batch_count.currentData() or 1)
		hdr = QLabel(f'Đã chọn {len(self.multi_topics)} ý tưởng — sẽ dùng {min(len(self.multi_topics), n)} cho lần chạy này')
		hdr.setStyleSheet('font-size:11px;color:#0A84FF;font-weight:600')
		self.multi_topic_lay.addWidget(hdr)
		for i, t in enumerate(self.multi_topics):
			row = QWidget()
			rh = QHBoxLayout(row)
			rh.setContentsMargins(0, 0, 0, 0)
			rh.setSpacing(6)
			lbl = QLabel(f"{i+1}. {t[:100]}")
			lbl.setStyleSheet('font-size:11px;color:#3A3A3C')
			lbl.setWordWrap(False)
			lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
			rh.addWidget(lbl, 1)
			rm = QPushButton("X")
			rm.setFixedSize(22, 22)
			rm.setStyleSheet('QPushButton{background:transparent;border:1px solid #E5E5EA;border-radius:4px;color:#8E8E93;font-weight:700;font-size:11px} QPushButton:hover{background:#FF453A;color:white;border-color:#FF453A}')
			rm.clicked.connect(lambda _=False, idx=i: self._remove_multi(idx))
			rh.addWidget(rm)
			self.multi_topic_lay.addWidget(row)

	def _remove_multi(self, idx):
		if 0 <= idx < len(self.multi_topics):
			self.multi_topics.pop(idx)
			self._render_multi_topics()

	def _apply_idea(self, idx):
		t = self.advisor_ideas.currentData()
		if t:
			self.topic.setText(t)
			self.logline('> Áp dụng: ' + t[:60])

	def _show_suggestions(self, title, suggestions):
		if not suggestions:
			return
		def _pick(it):
			ttl = str(it.get('title') or '')
			if ttl:
				self.topic.setText(ttl)
				self.logline('> Đã chọn: ' + ttl[:70])
		def _pick_multi(items):
			added = 0
			for it in items:
				ttl = str(it.get('title') or '').strip()
				if ttl and ttl not in self.multi_topics:
					self.multi_topics.append(ttl)
					added += 1
			self._render_multi_topics()
			self.logline(f'> Đã thêm {added} ý tưởng (tổng {len(self.multi_topics)})')
		dlg = SuggestDialog(title, suggestions, _pick, self, on_multi=_pick_multi)
		dlg.exec()
	def do_run(self):
		cid = self.ch.currentData()
		if cid is None:
			self.logline('! Chưa chọn kênh')
			return
		n = int(self.batch_count.currentData() or 1)
		base = {
			'channel_id': cid,
			'require_approval': (self.mode.currentIndex() == 1),
			'voice_override': self.voice.currentData(),
			'voice_preset': self.preset.currentData(),
		}
		k = self.kind.currentData()
		if k:
			base['kind'] = k
		lo = self.length.currentData()
		if lo:
			base['length_override'] = lo
		mods = {}
		for i, cb in enumerate(self.modules):
			cur = cb.currentData()
			if cur:
				mods[STEPS[i]['cat']] = cur
		mods['_opts'] = {'caption': self.chk_row.is_checked('caption'), 'music_only': self.chk_row.is_checked('music')}
		base['modules'] = mods
		if self.when.currentIndex() == 1:
			base['run_at'] = self.sched.dateTime().toString('yyyy-MM-dd HH:mm:ss')

		jids = []
		if self.multi_topics:
			use = self.multi_topics[:n]
			self.logline(f'> Tạo {len(use)} job, mỗi job 1 ý tưởng đã chọn')
			for idx, t in enumerate(use):
				b = dict(base)
				b['topic'] = t
				b['count'] = 1
				try:
					r = api.create_job(b)
				except Exception as e:
					self.logline(f'! Job {idx+1} API lỗi: ' + str(e)[:100])
					continue
				jid = r.get('job_id', r.get('id'))
				if not jid:
					self.logline(f'! Job {idx+1} không tạo được: ' + str(r)[:100])
					continue
				try:
					rr = api.run_job(jid)
				except Exception as e:
					self.logline(f'! Run job {idx+1} lỗi: ' + str(e)[:100])
					continue
				if rr.get('ok') is False:
					self.logline(f'! Run job {idx+1} fail: ' + str(rr)[:100])
					continue
				jids.append(jid)
				self.logline(f' > Job {idx+1}/{len(use)}: {jid} — {t[:60]}')
			remaining = n - len(use)
			if remaining > 0:
				self.logline(f'> Còn {remaining} video thiếu topic, tạo 1 job AI tự sinh')
				b = dict(base)
				b['topic'] = self.topic.text() or ''
				b['count'] = remaining
				try:
					r = api.create_job(b)
					jid = r.get('job_id', r.get('id'))
					if jid:
						rr = api.run_job(jid)
						if rr.get('ok') is not False:
							jids.append(jid)
				except Exception:
					pass
		else:
			body = dict(base)
			body['count'] = n
			body['topic'] = self.topic.text()
			self.logline('> Tạo job: kênh=' + str(cid) + ', số lượng=' + str(n))
			try:
				r = api.create_job(body)
			except Exception as e:
				self.logline('! Lỗi API: ' + str(e)[:150])
				return
			jid = r.get('job_id', r.get('id'))
			if not jid:
				self.logline('! Không tạo được job: ' + str(r)[:150])
				return
			try:
				rr = api.run_job(jid)
			except Exception as e:
				self.logline('! Lỗi chạy: ' + str(e)[:150])
				return
			if rr.get('ok') is False:
				self.logline('! Run lỗi: ' + str(rr)[:150])
				self._set_timeline_error()
				return
			jids.append(jid)

		if not jids:
			self._set_timeline_error()
			return
		self._jid = jids[0]
		self._jids = jids
		self._job_status = {}
		import time as _tm
		self._started = _tm.time()
		self._lastn = -1
		self._lastchange = _tm.time()
		self.btn_run.setEnabled(False)
		self.lbl_status.setText(f'Đang chạy {n} video ({len(jids)} job)...')
		self.timeline.set_state(0, TimelineStep.STATE_RUNNING)
		if not hasattr(self, 'timer'):
			self.timer = QTimer(self)
			self.timer.timeout.connect(self.poll_job)
		self.timer.start(1000)

	def _set_timeline_error(self):
		self.timeline.set_state(0, TimelineStep.STATE_ERROR)
		self.lbl_status.setText('Loi - kiem tra nhat ky' )
		self.btn_run.setEnabled(True)

	def poll_job(self):
		jids = getattr(self, '_jids', None) or ([self._jid] if getattr(self, '_jid', None) else [])
		if not jids:
			return
		import time, sqlite3
		try:
			cc = sqlite3.connect("state/pipeline.db")
			ph = ','.join('?' for _ in jids)
			n_row = cc.execute(f'SELECT COUNT() FROM publications WHERE job_id IN ({ph})', tuple(jids)).fetchone()
			n = int(n_row[0]) if n_row else 0
			jrows = cc.execute(f'SELECT id, status FROM jobs WHERE id IN ({ph})', tuple(jids)).fetchall()
			cc.close()
		except Exception:
			n = 0
			jrows = []
		if not hasattr(self, "_job_status"):
			self._job_status = {}
		for r in jrows:
			self._job_status[r[0]] = r[1]
		tail = []
		try:
			d = api.job_detail(jids[0])
			if isinstance(d, dict):
				tail = d.get('log_tail', []) or []
		except Exception:
			pass
		if tail:
			self.log.setPlainText(chr(10).join(tail))
			sb = self.log.verticalScrollBar()
			sb.setValue(sb.maximum())
		statuses = list(self._job_status.values())
		all_done = bool(statuses) and all(s in ('done', 'completed', 'success') for s in statuses)
		any_running = any(s in ('running', 'pending', 'queued') for s in statuses)
		any_error = any(s in ('error', 'failed') for s in statuses)
		total = int(self.batch_count.currentData() or 1)
		if n != self._lastn:
			self._lastn = n
			self._lastchange = time.time()
		if not self._started:
			self._started = time.time()
		el = int(time.time() - self._started)
		mins = el // 60
		secs = el % 60
		tstr = ((str(mins) + 'm ') if mins else '') + str(secs) + 's'
		if all_done:
			self.timer.stop()
			self.timeline.set_state(5, TimelineStep.STATE_DONE)
			self.lbl_status.setText(f'Hoàn tất {n} video / {tstr}')
			self.btn_run.setEnabled(True)
			self.logline(f'> Xong {n} video sau {tstr}')
		elif any_error and not any_running:
			self.timer.stop()
			self._set_timeline_error()
		elif any_running:
			step = min(4, n)
			self.timeline.set_state(step, TimelineStep.STATE_RUNNING)
			self.lbl_status.setText(f'Chạy {tstr} — {n}/{total} video')
