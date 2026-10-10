# -- coding: utf-8 --
# desktop_app/tray.py - System tray icon + menu
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
import urllib.request, json


def _status_text():
	try:
		r = urllib.request.urlopen('http://127.0.0.1:7777/api/health', timeout=2)
		d = json.loads(r.read().decode())
		pub = d.get('publications', 0)
		jb = d.get('jobs', 0)
		se = d.get('scheduler_error') or {}
		sch = 'ON' if se.get('alive') and not se.get('stale') else 'OFF'
		return "TNT Media | pub=" + str(pub) + " job=" + str(jb) + " | scheduler " + sch
	except Exception:
		return 'TNT Media | server OFF'


def attach(window, icon_path):
	app = QApplication.instance()
	if app is None or not QSystemTrayIcon.isSystemTrayAvailable():
		return None
	tray = QSystemTrayIcon(window)
	tray.setIcon(QIcon(icon_path))
	tray.setToolTip('TNT Media Studio')
	menu = QMenu()
	act_show = QAction('Hien thi')
	act_show.triggered.connect(lambda: (window.showNormal(), window.activateWindow()))
	menu.addAction(act_show)
	act_dash = QAction('Mo Dashboard')
	act_dash.triggered.connect(lambda: (window.showNormal(), window.go(0)))
	menu.addAction(act_dash)
	act_queue = QAction('Mo Hang doi video')
	act_queue.triggered.connect(lambda: (window.showNormal(), window.go(3)))
	menu.addAction(act_queue)
	act_pipe = QAction('Mo Quy trinh')
	act_pipe.triggered.connect(lambda: (window.showNormal(), window.go(2)))
	menu.addAction(act_pipe)
	menu.addSeparator()
	act_status = QAction('Trang thai')
	act_status.triggered.connect(lambda: tray.showMessage('TNT Media', _status_text(), QSystemTrayIcon.Information, 4000))
	menu.addAction(act_status)
	menu.addSeparator()
	act_quit = QAction('Thoat')
	act_quit.triggered.connect(app.quit)
	menu.addAction(act_quit)
	tray.setContextMenu(menu)
	def on_click(reason):
		if reason == QSystemTrayIcon.Trigger:
			window.showNormal()
			window.activateWindow()
	tray.activated.connect(on_click)
	tray.show()
	return tray
