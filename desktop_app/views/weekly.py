# -*- coding: utf-8 -*-
# desktop_app/views/weekly.py - Weekly batch video generator (1 week x N channels).
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox,
    QSpinBox, QPlainTextEdit, QMessageBox, QProgressBar, QFrame, QGridLayout,
    QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
import api, i18n
from widgets import PageHeader, busy_wrap


class Weekly(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_pid = None
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = PageHeader(
            i18n.t('nav.weekly') if i18n.t('nav.weekly') != 'nav.weekly' else 'Tạo video tự động',
            i18n.t('weekly.sub') if i18n.t('weekly.sub') != 'weekly.sub' else 'Tự tạo đủ video cho 1 tuần, chất lượng 100 điểm'
        )
        root.addWidget(self.header)

        body = QVBoxLayout()
        body.setContentsMargins(20, 16, 20, 16)
        body.setSpacing(12)

        # ---- Controls ----
        card = QFrame()
        card.setObjectName('Card')
        cg = QGridLayout(card)
        cg.setContentsMargins(16, 14, 16, 14)
        cg.setHorizontalSpacing(14)
        cg.setVerticalSpacing(10)

        row = 0
        cg.addWidget(QLabel('Số ngày:'), row, 0)
        self.sp_days = QSpinBox()
        self.sp_days.setRange(1, 30)
        self.sp_days.setValue(7)
        cg.addWidget(self.sp_days, row, 1)

        cg.addWidget(QLabel('Video/ngày/kênh:'), row, 2)
        self.sp_per_day = QSpinBox()
        self.sp_per_day.setRange(1, 5)
        self.sp_per_day.setValue(2)
        cg.addWidget(self.sp_per_day, row, 3)

        cg.addWidget(QLabel('Điểm tối thiểu:'), row, 4)
        self.sp_score = QSpinBox()
        self.sp_score.setRange(80, 100)
        self.sp_score.setValue(100)
        cg.addWidget(self.sp_score, row, 5)

        row = 1
        cg.addWidget(QLabel('Kênh:'), row, 0)
        self.cb_channel = QComboBox()
        self.cb_channel.addItem('Tất cả kênh đang bật', None)
        cg.addWidget(self.cb_channel, row, 1, 1, 3)

        self.btn_start = QPushButton('Tạo video 1 tuần')
        self.btn_start.setObjectName('Primary')
        self.btn_start.setMinimumHeight(40)
        self.btn_start.clicked.connect(self.start)
        cg.addWidget(self.btn_start, row, 4, 1, 2)

        body.addWidget(card)

        # ---- Status card ----
        sc = QFrame()
        sc.setObjectName('Card')
        sv = QVBoxLayout(sc)
        sv.setContentsMargins(16, 14, 16, 14)
        sv.setSpacing(8)

        top = QHBoxLayout()
        self.lbl_phase = QLabel('Sẵn sàng')
        self.lbl_phase.setStyleSheet('font-size:15px;font-weight:700;color:#0A84FF')
        self.lbl_phase.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.lbl_phase.setMinimumWidth(0)
        top.addWidget(self.lbl_phase, 1)

        self.btn_stop = QPushButton('Dừng')
        self.btn_stop.setObjectName('Danger')
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop)
        top.addWidget(self.btn_stop)

        self.btn_refresh = QPushButton('Làm mới')
        self.btn_refresh.clicked.connect(self.refresh)
        top.addWidget(self.btn_refresh)
        sv.addLayout(top)

        self.pb = QProgressBar()
        self.pb.setRange(0, 100)
        self.pb.setValue(0)
        self.pb.setFormat('%v%')
        sv.addWidget(self.pb)

        stats = QHBoxLayout()
        self.lbl_done = QLabel('0/0')
        self.lbl_100 = QLabel('100đ:0')
        self.lbl_below = QLabel('<100:0')
        self.lbl_reject = QLabel('bỏ:0')
        self.lbl_elapsed = QLabel('')
        for w in (self.lbl_done, self.lbl_100, self.lbl_below, self.lbl_reject, self.lbl_elapsed):
            w.setStyleSheet('color:#8E8E93;font-size:12px;padding-right:10px')
            w.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            w.setMinimumWidth(0)
            stats.addWidget(w)
        stats.addStretch()
        sv.addLayout(stats)

        self.cur = QLabel('')
        self.cur.setStyleSheet('color:#3A3A3C;font-size:12px;font-family:Consolas,monospace')
        self.cur.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.cur.setMinimumWidth(0)
        sv.addWidget(self.cur)

        body.addWidget(sc)

        # ---- Log ----
        body.addWidget(QLabel('Nhật ký chạy (30 dòng cuối):'))
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet('font-family:Consolas,monospace;font-size:11px')
        self.log.setMaximumBlockCount(400)
        body.addWidget(self.log, 1)

        root.addLayout(body)

        self._t = QTimer(self)
        self._t.timeout.connect(self.refresh)
        self._t.start(3000)
        self.load_channels()
        self.refresh()

    def load_channels(self):
        try:
            d = api.channels()
            items = d.get('channels', d.get('items', []))
            for it in items:
                if isinstance(it, dict):
                    cid = it.get('id')
                    if cid:
                        self.cb_channel.addItem(str(cid), cid)
        except Exception:
            pass

    def _parse(self, r):
        if not isinstance(r, dict):
            return {}
        return r

    def start(self):
        st = self._parse(api.weekly_status())
        if st.get('alive') or st.get('running'):
            if QMessageBox.question(self, 'Đang chạy', 'Batch đang chạy. Dừng rồi tạo mới?') != QMessageBox.Yes:
                return
            try:
                api.weekly_stop()
            except Exception:
                pass

        days = int(self.sp_days.value())
        per_day = int(self.sp_per_day.value())
        score = int(self.sp_score.value())
        ch = self.cb_channel.currentData()
        n_channels = 1 if ch else 2
        estimate = days * per_day * n_channels
        msg = (
            'Tạo ' + str(estimate) + ' video (' + str(days) + ' ngày x ' + str(per_day)
            + '/ngày x ' + str(n_channels) + ' kênh)?\n\n'
            'Điểm tối thiểu: ' + str(score) + '/100\n'
            'Quá trình render có thể mất 1-4 tiếng tuỳ engine.\n'
            'Video đạt sẽ vào Hàng đợi để đăng theo lịch tối ưu.'
        )
        if QMessageBox.question(self, 'Tạo video 1 tuần', msg) != QMessageBox.Yes:
            return
        payload = {
            'days': days,
            'per_day': per_day,
            'min_score': score,
            'channels': [ch] if ch else [],
        }
        r = busy_wrap(self, lambda: api.weekly_start(payload), 'Đang khởi động batch...')
        r = self._parse(r)
        if not r.get('ok'):
            QMessageBox.warning(self, 'Lỗi', str(r.get('error') or r)[:500])
            return
        self._last_pid = r.get('pid')
        QMessageBox.information(self, 'Đã bắt đầu',
            'Batch đã chạy nền (pid ' + str(self._last_pid) + ').\n'
            'Theo dõi tiến độ ở đây, có thể đóng tab và quay lại sau.')
        self.refresh()

    def stop(self):
        if QMessageBox.question(self, 'Dừng', 'Dừng batch? Video đang render dở sẽ bị hủy.') != QMessageBox.Yes:
            return
        r = busy_wrap(self, lambda: api.weekly_stop(), 'Đang dừng...')
        r = self._parse(r)
        if not r.get('ok'):
            QMessageBox.warning(self, 'Lỗi', str(r.get('error') or r)[:300])
        self.refresh()

    def refresh(self):
        try:
            r = api.weekly_status()
        except Exception as e:
            self.lbl_phase.setText('Lỗi kết nối: ' + str(e)[:80])
            self.lbl_phase.setStyleSheet('font-size:15px;font-weight:700;color:#FF453A')
            return
        r = self._parse(r)
        phase = str(r.get('phase') or 'idle')
        alive = bool(r.get('alive'))
        running = bool(r.get('running'))
        labels = {
            'idle': 'Sẵn sàng',
            'starting': 'Đang khởi động...',
            'generating_content': 'Đang tạo nội dung AI...',
            'rendering': 'Đang render video...',
            'scheduling': 'Đang lên lịch đăng...',
            'done': 'Hoàn tất',
            'error': 'Lỗi',
            'stopped': 'Đã dừng',
            'dry_run': 'Chạy thử',
        }
        color = '#0A84FF'
        if phase == 'done':
            color = '#34C759'
        elif phase in ('error',):
            color = '#FF453A'
        elif phase == 'stopped':
            color = '#FF9500'
        self.lbl_phase.setText(labels.get(phase, phase))
        self.lbl_phase.setStyleSheet('font-size:15px;font-weight:700;color:' + color)

        total = int(r.get('total_planned') or 0)
        done = int(r.get('completed') or 0)
        pct = int(round(done * 100 / total)) if total else 0
        self.pb.setValue(max(0, min(100, pct)))
        self.pb.setFormat(str(done) + '/' + str(total) + ' (%v%)' if total else '%v%')
        self.lbl_done.setText('Hoàn thành: ' + str(done) + '/' + str(total))
        self.lbl_100.setText('100đ: ' + str(int(r.get('accepted_100') or 0)))
        self.lbl_below.setText('dưới 100: ' + str(int(r.get('accepted_below') or 0)))
        self.lbl_reject.setText('bỏ: ' + str(int(r.get('rejected') or 0)))
        el = r.get('elapsed_sec')
        if el:
            self.lbl_elapsed.setText('thời gian: ' + str(el) + 's')
        else:
            self.lbl_elapsed.setText('')

        cur = r.get('current')
        if cur:
            self.cur.setText('▸ ' + str(cur))
        else:
            self.cur.setText('')

        self.btn_stop.setEnabled(alive)
        self.btn_start.setEnabled(not alive)

        tail = r.get('log_tail') or []
        if tail:
            txt = chr(10).join(tail)
            self.log.setPlainText(txt)
            sb = self.log.verticalScrollBar()
            sb.setValue(sb.maximum())

        if r.get('error'):
            self.cur.setText('Lỗi: ' + str(r.get('error'))[:300])
            self.cur.setStyleSheet('color:#FF453A;font-size:12px;font-family:Consolas,monospace')
        else:
            self.cur.setStyleSheet('color:#3A3A3C;font-size:12px;font-family:Consolas,monospace')
