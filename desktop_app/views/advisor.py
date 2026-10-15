# -- coding: utf-8 --
# desktop_app/views/advisor.py - Ask Studio noi bo
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit)
from PySide6.QtCore import Qt, QThread, Signal
import api, i18n
from widgets import PageHeader

class AdvWorker(QThread):
	done = Signal(dict)
	def __init__(self, force=0):
		super().__init__()
		self.force = force
	def run(self):
		r = api.get('/api/studio/advice?force=' + str(self.force), timeout=200)
		self.done.emit(r or {})

class Advisor(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		root = QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)
		self.header = PageHeader(i18n.t('nav.advisor'), i18n.t('advisor.sub'))
		root.addWidget(self.header)
		body = QVBoxLayout()
		body.setContentsMargins(20, 16, 20, 16)
		body.setSpacing(12)
		bar = QHBoxLayout()
		self.btn = QPushButton(i18n.t('advisor.btn.run'))
		self.btn.setMinimumHeight(36)
		self.btn.clicked.connect(lambda: self.run_analysis(0))
		self.btn2 = QPushButton(i18n.t('advisor.btn.force'))
		self.btn2.setMinimumHeight(36)
		self.btn2.clicked.connect(lambda: self.run_analysis(1))
		self.btn3 = QPushButton(i18n.t('advisor.btn.history'))
		self.btn3.setMinimumHeight(36)
		self.btn3.clicked.connect(self.show_history)
		self.status = QLabel(i18n.t('advisor.hint'))
		bar.addWidget(self.btn)
		bar.addWidget(self.btn2)
		bar.addWidget(self.btn3)
		bar.addWidget(self.status, 1)
		body.addLayout(bar)
		self.out = QTextEdit()
		self.out.setReadOnly(True)
		self.out.setStyleSheet('font-size:13px; padding:10px')
		body.addWidget(self.out, 1)
		root.addLayout(body)
	def run_analysis(self, force):
		self.status.setText(i18n.t('advisor.running'))
		self.out.setPlainText('')
		self.btn.setEnabled(False)
		self.btn2.setEnabled(False)
		self.worker = AdvWorker(force=force)
		self.worker.done.connect(self.show_result)
		self.worker.start()
	def show_history(self):
		import json as _j
		r = api.get('/api/studio/history?limit=10')
		items = (r or {}).get('items', [])
		L = [i18n.t('advisor.history.title'), '']
		for it in items:
			L.append(str(it.get('file')) + ' ideas=' + str(it.get('ideas')) )
			L.append(' ' + str(it.get('summary',''))[:180])
			L.append('')
		self.out.setPlainText(chr(10).join(L))
		self.status.setText('History: ' + str(len(items)) + ' entries')
	def show_result(self, r):
		self.btn.setEnabled(True)
		self.btn2.setEnabled(True)
		if not r.get('ok'):
			self.status.setText('Loi: ' + str(r.get('error', 'unknown'))[:120])
			return
		self.status.setText('OK | cached=' + str(r.get('cached')))
		a = r.get('advisor') or {}
		ch = r.get('channel') or {}
		L = []
		L.append(i18n.t('advisor.result.channel'))
		L.append('Ten: ' + str(ch.get('title')))
		L.append('Subs: ' + str(ch.get('subs')) + ' Views: ' + str(ch.get('views_total')) + ' Videos: ' + str(ch.get('videos_total')))
		L.append('')
		L.append(i18n.t('advisor.result.summary'))
		L.append(str(a.get('summary', '')))
		L.append('')
		L.append(i18n.t('advisor.result.strengths'))
		for s in (a.get('strengths') or []):
			L.append('+ ' + str(s))
		L.append('')
		L.append(i18n.t('advisor.result.weaknesses'))
		for s in (a.get('weaknesses') or []):
			L.append('- ' + str(s))
		L.append('')
		L.append(i18n.t('advisor.result.patterns'))
		for s in (a.get('patterns') or []):
			L.append('* ' + str(s))
		L.append('')
		L.append(i18n.t('advisor.result.ideas'))
		for i, x in enumerate((a.get('next_ideas') or []), 1):
			L.append(str(i) + '. ' + str(x.get('title')))
			L.append(' Hook: ' + str(x.get('hook')))
			L.append(' Ly do: ' + str(x.get('why')))
		L.append('')
		L.append(i18n.t('advisor.result.actions'))
		for s in (a.get('actions') or []):
			L.append('> ' + str(s))
		self.out.setPlainText(chr(10).join(L))
