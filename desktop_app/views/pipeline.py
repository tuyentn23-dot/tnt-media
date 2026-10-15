from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QComboBox, QFrame, QTextEdit, QLineEdit, QDateTimeEdit, QProgressBar, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt
import i18n, api
from widgets import PageHeader

STEPS = [
	{'key': 'pipe.step.analyze', 'cat': 'analyze', 'color': '#FF375F', 'num': '0'},
	{'key': 'pipe.step.content', 'cat': 'content', 'color': '#34C759', 'num': '1'},
	{'key': 'pipe.step.render', 'cat': 'render', 'color': '#0A84FF', 'num': '2'},
	{'key': 'pipe.step.voice', 'cat': 'voice', 'color': '#AF52DE', 'num': '3'},
	{'key': 'pipe.step.publish', 'cat': 'publish', 'color': '#FF9500', 'num': '4'},
]
STATES = {'idle': '#8E8E93', 'queued': '#FF9500', 'running': '#0A84FF', 'done': '#34C759', 'error': '#FF453A'}

class StepCard(QFrame):
	def __init__(self, info, parent=None):
		super().__init__(parent)
		self.setObjectName('Card')
		self.info = info
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		self.setMaximumWidth(220)
		lay = QVBoxLayout(self)
		lay.setContentsMargins(8, 6, 8, 6)
		lay.setSpacing(4)
		head = QHBoxLayout()
		dot = QLabel()
		dot.setFixedSize(14, 14)
		dot.setStyleSheet('background:' + info['color'] + ';border-radius:7px')
		num = QLabel(info['num'])
		num.setStyleSheet('font-weight:700;color:#8E8E93')
		ttl = QLabel(i18n.t(info['key']))
		ttl.setStyleSheet('font-weight:700;font-size:12px')
		head.addWidget(dot)
		head.addWidget(num)
		head.addWidget(ttl)
		head.addStretch()
		self.badge = QLabel(i18n.t('pipe.idle'))
		self.badge.setStyleSheet('color:#8E8E93;font-size:11px;font-weight:600')
		head.addWidget(self.badge)
		lay.addLayout(head)
		self.mod = QComboBox()
		self.mod.setMinimumWidth(0)
		self.mod.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
		self.mod.setMinimumContentsLength(12)
		self.mod.currentIndexChanged.connect(self._on_mod_change)
		lay.addWidget(self.mod)
		self.hint = QLabel('')
		self.hint.setWordWrap(False)
		self.hint.setStyleSheet('color:#4f8cff;font-size:10px;padding:1px 0')
		self.hint.setMinimumHeight(16)
		self.hint.setMaximumHeight(16)
		lay.addWidget(self.hint)
		self.bar = QProgressBar()
		self.bar.setRange(0, 100)
		self.bar.setValue(0)
		self.bar.setTextVisible(False)
		self.bar.setFixedHeight(4)
		lay.addWidget(self.bar)
		self._meta = {}
		self.msg = QLabel('')

	def _on_mod_change(self):
		d = getattr(self, '_meta', {}) or {}
		cur = self.mod.currentData()
		if not cur:
			self.hint.setText(i18n.t('pipe.hint_empty'))
			return
		m = d.get(cur, {}) or {}
		w = str(m.get('when') or '')[:70]
		self.hint.setText(w if w else i18n.t('pipe.hint_empty'))

	def set_status(self, state, msg='', pct=None):
		c = STATES.get(state, '#8E8E93')
		self.badge.setText(i18n.t('pipe.' + state))
		self.badge.setStyleSheet('color:' + c + ';font-size:11px;font-weight:700')
		if state == 'running':
			if pct is None:
				self.bar.setRange(0, 0)
			else:
				self.bar.setRange(0, 100)
				self.bar.setValue(int(pct))
			css = 'QProgressBar::chunk { background: ' + c + '; }'
			self.bar.setStyleSheet(css)
		elif state == 'done':
			self.bar.setRange(0, 100)
			self.bar.setValue(100)
			self.bar.setStyleSheet('QProgressBar::chunk { background: ' + c + '; }')
		elif state == 'error':
			self.bar.setRange(0, 100)
			self.bar.setValue(100)
			self.bar.setStyleSheet('QProgressBar::chunk { background: ' + c + '; }')
		else:
			self.bar.setRange(0, 100)
			self.bar.setValue(0)
			self.bar.setStyleSheet('')
		if msg:
			self.msg.setText(msg)

class Pipeline(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t('nav.pipeline'), i18n.t('pipe.title'))
		root.addWidget(self.header)
		body = QVBoxLayout()
		body.setContentsMargins(14, 8, 14, 8)
		body.setSpacing(6)
		# HANG 1: channel + kind + length + mode + when + schedule
		row1 = QHBoxLayout()
		row1.setSpacing(6)
		row1.addWidget(QLabel(i18n.t('pipe.channel') + ':'))
		self.ch = QComboBox()
		self.ch.setMinimumWidth(110)
		self.ch.currentIndexChanged.connect(self.load_kinds)
		row1.addWidget(self.ch)
		row1.addWidget(QLabel('Kind:'))
		self.kind = QComboBox()
		self.kind.setMinimumWidth(90)
		row1.addWidget(self.kind)
		row1.addWidget(QLabel(i18n.t('pipe.length') + ':'))
		self.length = QComboBox()
		self.length.addItem(i18n.t('pipe.short'), None)
		self.length.addItem(i18n.t('pipe.long'), 90)
		row1.addWidget(self.length)
		row1.addWidget(QLabel(i18n.t('pipe.mode') + ':'))
		self.mode = QComboBox()
		self.mode.addItems([i18n.t('pipe.auto'), i18n.t('pipe.manual')])
		row1.addWidget(self.mode)
		row1.addWidget(QLabel(i18n.t('pipe.when') + ':'))
		self.when = QComboBox()
		self.when.addItems([i18n.t('pipe.now'), i18n.t('pipe.schedule')])
		row1.addWidget(self.when)
		from PySide6.QtCore import QDateTime
		self.sched = QDateTimeEdit()
		self.sched.setCalendarPopup(True)
		self.sched.setDateTime(QDateTime.currentDateTime().addSecs(3600))
		self.sched.setDisplayFormat('yyyy-MM-dd HH:mm')
		self.sched.setVisible(False)
		self.when.currentIndexChanged.connect(self.on_when_changed)
		row1.addWidget(self.sched)
		row1.addStretch()
		body.addLayout(row1)
		# HANG 2: topic + trend + analyze + voice + preset + advisor ideas
		row2 = QHBoxLayout()
		row2.setSpacing(6)
		row2.addWidget(QLabel(i18n.t('pipe.topic') + ':'))
		self.topic = QLineEdit()
		self.topic.setPlaceholderText(i18n.t('pipe.topic_hint'))
		row2.addWidget(self.topic, 1)
		self.btn_trend = QPushButton(i18n.t('pipe.trend_btn'))
		self.btn_trend.clicked.connect(self.do_trend)
		row2.addWidget(self.btn_trend)
		self.btn_adv = QPushButton(i18n.t('pipe.advisor.load'))
		self.btn_adv.clicked.connect(self.load_advisor)
		row2.addWidget(self.btn_adv)
		self.advisor_ideas = QComboBox()
		self.advisor_ideas.setMinimumWidth(140)
		self.advisor_ideas.addItem(i18n.t('pipe.advisor.pick'), None)
		self.advisor_ideas.currentIndexChanged.connect(self.apply_idea)
		row2.addWidget(self.advisor_ideas)
		row2.addWidget(QLabel(i18n.t('pipe.voice') + ':'))
		self.voice = QComboBox()
		self.voice.setMinimumWidth(110)
		row2.addWidget(self.voice)
		row2.addWidget(QLabel(i18n.t('pipe.preset') + ':'))
		self.preset = QComboBox()
		self.preset.setMinimumWidth(90)
		row2.addWidget(self.preset)
		body.addLayout(row2)
		# HANG 3: 5 step cards trong 1 hang (5 cot)
		steps_box = QHBoxLayout()
		steps_box.setSpacing(6)
		self.steps = []
		for i, info in enumerate(STEPS):
			c = StepCard(info)
			steps_box.addWidget(c, 1)
			self.steps.append(c)
		body.addLayout(steps_box)
		# HANG 4: log
		self.log = QTextEdit()
		self.log.setReadOnly(True)
		self.log.setMinimumHeight(50)
		self.log.setMaximumHeight(90)
		body.addWidget(self.log, 1)
		# HANG 5: run button
		bottom = QHBoxLayout()
		bottom.addStretch()
		self.run = QPushButton(i18n.t('pipe.run'))
		self.run.setObjectName('Primary')
		self.run.setMinimumHeight(32)
		self.run.setMinimumWidth(160)
		self.run.clicked.connect(self.do_run)
		bottom.addWidget(self.run)
		body.addLayout(bottom)
		root.addLayout(body)
		self.load_channels()
		self.load_kinds()
		self.load_modules()
		self.load_voice_presets()

	def logline(self, txt):
		self.log.append(txt)

	def load_channels(self):
		d = api.channels()
		items = d.get('channels', d.get('items', d if isinstance(d, list) else []))
		self.ch.clear()
		if not items:
			self.ch.addItem('Chưa có kênh', None)
		for it in items:
			if isinstance(it, dict):
				nm = str(it.get('name', it.get('id')))
				iid = it.get('id')
			else:
				nm = str(it)
				iid = it
			self.ch.addItem(nm, iid)

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
		meta_by_name = {}
		for it in items:
			if not isinstance(it, dict):
				continue
			cat = it.get('category', 'other')
			name = it.get('name', '?')
			ver = it.get('version', '')
			label = name + ' v' + str(ver)
			by.setdefault(cat, []).append(label)
			meta_by_name[label] = {
				'name': name,
				'title': it.get('title', ''),
				'desc': it.get('desc', ''),
				'when': it.get('when_to_use', ''),
				'note': it.get('note', ''),
			}
		self._mod_meta = meta_by_name
		for c in self.steps:
			cat = c.info['cat']
			c.mod.clear()
			c.mod.addItem(i18n.t('pipe.select_module'), None)
			for lbl in by.get(cat, []):
				c.mod.addItem(lbl, lbl)
			c._meta = meta_by_name
			if not by.get(cat):
				c.msg.setText(i18n.t('common.none'))

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

	def set_all(self, state, msg='', pct=None):
		for c in self.steps:
			c.set_status(state, msg, pct)

	def do_trend(self):
		self.logline('> Dang thu thap xu huong...')
		try:
			rc = api.post('/api/trends/collect', {})
			self.logline(' Thu thap: ' + str(rc.get('collected', 0)) + ' / luu: ' + str(rc.get('saved', 0)) + ' moi')
		except Exception as e:
			self.logline(' Loi collect: ' + str(e))
		try:
			d = api.get('/api/trends')
			items = d.get('items', [])
			self.logline(' Tong trend trong DB: ' + str(len(items)) + ' xu huong')
			for it in items[:10]:
				if isinstance(it, dict):
					kw = it.get('topic', it.get('keyword', '?'))
					sc = it.get('score', '?')
					self.logline(' - ' + str(kw)[:70] + ' (score=' + str(sc) + ')')
		except Exception as e:
			self.logline(' Loi doc trends: ' + str(e))
	def do_analyze(self):
		self.logline('> Phan tich video da dang...')
		try:
			d = api.publications()
			items = d.get('items', d if isinstance(d, list) else [])
			n = len(items)
			self.logline(' Tong so: ' + str(n) + ' video')
			by = {}
			bych = {}
			for x in items:
				if not isinstance(x, dict):
					continue
				st = str(x.get('status') or '?')
				by[st] = by.get(st, 0) + 1
				ch = str(x.get('channel_id') or '?')
				bych[ch] = bych.get(ch, 0) + 1
			self.logline(' Theo trang thai:')
			for k in by:
				self.logline(' ' + str(k) + ': ' + str(by[k]))
			self.logline(' Theo kenh:')
			for k in bych:
				self.logline(' ' + str(k) + ': ' + str(bych[k]))
			pub = by.get('published', 0)
			rend = by.get('rendered', 0)
			self.logline(' => Da dang that: ' + str(pub) + ' | Cho duyet: ' + str(rend))
		except Exception as e:
			self.logline(' Loi: ' + str(e))
	def load_advisor(self, force=False):
		self.logline('> Lay goi y tu Advisor...')
		try:
			url = '/api/studio/advice?force=' + ('1' if force else '0')
			cid = self.ch.currentData()
			if cid:
				url = url + '&channel_id=' + str(cid)
			d = api.get(url)
			adv = (d or {}).get('advisor') or {}
			summary = adv.get('summary') or i18n.t('pipe.advisor.none')
			self.advisor_ideas.clear()
			self.advisor_ideas.addItem(i18n.t('pipe.advisor.pick'), None)
			for idea in (adv.get('next_ideas') or []):
				ttl = (idea.get('title') or '')[:80]
				if ttl:
					self.advisor_ideas.addItem(ttl, ttl)
			self.logline(' Advisor OK: ' + str(len(adv.get('next_ideas') or [])) + ' y tuong')
		except Exception as e:
			self.logline('! Advisor loi: ' + str(e)[:120])

	def apply_idea(self, idx):
		t = self.advisor_ideas.currentData()
		if t:
			self.topic.setText(t)
			self.logline('> Ap dung y tuong: ' + t[:60])

	def on_when_changed(self, idx):
		self.sched.setVisible(idx == 1)
	def do_run(self):
		cid = self.ch.currentData()
		if cid is None:
			self.logline('! Chua chon kenh')
			return
		body = {'channel_id': cid}
		k = self.kind.currentData()
		if k:
			body['kind'] = k
		lo = self.length.currentData()
		if lo:
			body['length_override'] = lo
		body['topic'] = self.topic.text()
		body['require_approval'] = (self.mode.currentIndex() == 1)
		body['voice_override'] = self.voice.currentData()
		body['voice_preset'] = self.preset.currentData()
		# Thu thap modules user chon
		mods = {}
		for c in self.steps:
			cat = c.info['cat']
			cur = c.mod.currentData()
			if cur:
				mods[cat] = cur
		body['modules'] = mods
		if self.when.currentIndex() == 1:
			body['run_at'] = self.sched.dateTime().toString('yyyy-MM-dd HH:mm:ss')
		self.logline('> Tao cong viec: ' + str(body))
		r = api.create_job(body)
		self.logline(str(r))
		jid = r.get('job_id', r.get('id'))
		if not jid:
			self.logline('! Khong tao duoc cong viec')
			return
		self.logline('> Dang chay: ' + str(jid))
		rr = api.run_job(jid)
		self.logline(str(rr))
		if rr.get('ok') is False:
			self.set_all('error')
			return
		self._jid = jid
		import time as _tm
		self._started = _tm.time()
		self._lastn = -1
		self._lastchange = _tm.time()
		self.set_all('queued')
		for c in self.steps:
			c.set_status('running')
		if not hasattr(self, 'timer'):
			from PySide6.QtCore import QTimer
			self.timer = QTimer(self)
			self.timer.timeout.connect(self.poll_job)
		self.timer.start(1000)

	def poll_job(self):
		jid = getattr(self, '_jid', None)
		if not jid:
			return
		import time
		d = api.job_detail(jid)
		if not isinstance(d, dict) or d.get('ok') is False:
			return
		tail = d.get('log_tail', [])
		if tail:
			self.log.setPlainText(chr(10).join(tail))
			sb = self.log.verticalScrollBar()
			sb.setValue(sb.maximum())
		st = str(d.get('status') or '')
		# Dem tu DB
		try:
			import sqlite3
			cc = sqlite3.connect('state/pipeline.db')
			row = cc.execute('SELECT COUNT() FROM publications WHERE job_id=?', (jid,)).fetchone()
			n = int(row[0]) if row else 0
			cc.close()
		except Exception:
			n = len([x for x in tail if 'rendered' in x])
		total = int(d.get('count') or 1)
		running = bool(d.get('running'))
		if not hasattr(self, '_started'):
			self._started = time.time()
		el = int(time.time() - getattr(self, '_started', time.time()))
		mins = el // 60
		secs = el % 60
		tstr = ((str(mins) + 'm ') if mins else '') + str(secs) + 's'
		pct = min(99, int(n * 100 / max(1, total))) if running else (100 if st in ('done', 'completed', 'success', 'error', 'failed') else 0)
		eta = ''
		if n > 0 and running and el > 5:
			rate = el / n
			remain = max(0, int(rate * (total - n)))
			eta = ' - con ~' + str(remain // 60) + 'm ' + str(remain % 60) + 's'
		lastn = getattr(self, '_lastn', -1)
		if n != lastn:
			self._lastn = n
			self._lastchange = time.time()
		stall = int(time.time() - getattr(self, '_lastchange', time.time()))
		if st in ('done', 'completed', 'success'):
			self.timer.stop()
			self.set_all('done', str(n) + ' video / ' + tstr, 100)
			self.logline('> Hoan tat sau ' + tstr + ': ' + str(n) + ' video')
		elif st in ('error', 'failed'):
			self.timer.stop()
			self.set_all('error', 'Loi sau ' + tstr, 100)
		elif running or st in ('running', 'pending', 'queued'):
			msg = 'Chay ' + tstr + ' - ' + str(n) + '/' + str(total) + ' video' + eta
			if stall >= 30:
				msg = msg + ' [khong tien trien ' + str(stall) + 's]'
			self.set_all('running', msg, pct)
