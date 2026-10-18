# -- coding: utf-8 --
# desktop_app/icons.py - SF-Symbols-style inline SVG icons
from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

_PATHS = {
	'dashboard': 'M3 12l9-9 9 9M5 10v10h14V10',
	'channels': 'M4 5h16v12H4zM8 21h8M12 17v4',
	'pipeline': 'M3 6h6v4H3zM3 14h6v4H3zM13 8h8M13 16h8M9 8h4M9 16h4',
	'queue': 'M4 6h16M4 12h16M4 18h10',
	'jobs': 'M4 6h16v14H4zM4 10h16M9 6v14',
	'pubs': 'M12 3v12M8 11l4 4 4-4M5 21h14',
	'modules': 'M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5M3 17l9 5 9-5',
	'settings': 'M12 9a3 3 0 100 6 3 3 0 000-6zM19 12l2-1-2-3-2 1-2-1-1-2h-4l-1 2-2 1-2-1-2 3 2 1v2l-2 1 2 3 2-1 2 1 1 2h4l1-2 2-1 2 1 2-3-2-1z',
	'search': 'M11 4a7 7 0 105.2 12.2L21 21M11 4a7 7 0 015.2 12.2',
	'play': 'M6 4l14 8-14 8z',
	'check': 'M4 12l5 5L20 6',
	'chevron_down': 'M6 9l6 6 6-6',
	'plus': 'M12 5v14M5 12h14',
	'sparkle': 'M12 3l2 5 5 2-5 2-2 5-2-5-5-2 5-2 2-5z',
	'trend': 'M3 17l6-6 4 4 8-8M15 7h6v6',
	'clock': 'M12 3a9 9 0 100 18 9 9 0 000-18zM12 7v5l3 3',
	'studio': 'M3 12l9-9 9 9M5 10v10h14V10',
	'library': 'M4 6h4v14H4zM10 6h4v14h-4zM16 6h4v14h-4z',
}

def svg(path_d, color='#1D1D1F', width=1.8):
	return (
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
		'fill="none" stroke="' + color + '" stroke-width="' + str(width) +
		'" stroke-linecap="round" stroke-linejoin="round">'
		'<path d="' + path_d + '"/></svg>'
	)

def pixmap(name, size=20, color='#1D1D1F', width=1.8):
	d = _PATHS.get(name)
	if not d:
		return QPixmap()
	renderer = QSvgRenderer(QByteArray(svg(d, color, width).encode('utf-8')))
	pm = QPixmap(size, size)
	pm.fill(Qt.transparent)
	p = QPainter(pm)
	p.setRenderHint(QPainter.Antialiasing, True)
	renderer.render(p)
	p.end()
	return pm

def icon(name, size=20, color='#1D1D1F', width=1.8):
	return QIcon(pixmap(name, size, color, width))
