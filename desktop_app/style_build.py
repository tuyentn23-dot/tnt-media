# -- coding: utf-8 --
# desktop_app/style_build.py - QSS generator matching redesign v2 mockup
from tokens import palette

def build(theme='light'):
	p = palette(theme)
	q = []
	a = q.append

	# Base
	a('QWidget{background:%s;color:%s;font-family:-apple-system,"Segoe UI",Roboto,sans-serif;font-size:13px}' % (p['bg'], p['label']))
	a('QMainWindow,QDialog{background:%s}' % p['bg'])
	a('QLabel{background:transparent}')

	# Sidebar
	a('#Sidebar{background:%s;border-right:1px solid %s}' % (p['surface'], p['sep']))
	a('#Sidebar QLabel#Brand{font-size:22px;font-weight:800;color:%s;padding:4px 8px}' % p['accent'])
	a('#Sidebar QLabel#BrandSub{font-size:11px;color:%s;padding:0 8px 20px 8px}' % p['label3'])
	a('#Sidebar QPushButton{background:transparent;border:none;text-align:left;padding:10px 12px;border-radius:8px;color:%s;font-size:13px;margin:2px 0}' % p['label2'])
	a('#Sidebar QPushButton:hover{background:%s}' % p['ctrl_hover'])
	a('#Sidebar QPushButton:checked{background:%s;color:%s;font-weight:600}' % (p['sidebar_sel'], p['accent']))

	# TopBar
	a('#TopBar{background:%s;border-bottom:1px solid %s}' % (p['surface'], p['sep']))

	# PageHeader
	a('#PageTitle{font-size:22px;font-weight:700;color:%s}' % p['label'])
	a('#PageSub{font-size:12px;color:%s}' % p['label3'])

	# Cards
	a('#Card{background:%s;border:1px solid %s;border-radius:12px}' % (p['surface'], p['sep']))
	a('#Group{background:%s;border:1px solid %s;border-radius:12px}' % (p['surface'], p['sep']))
	a('#CardHeader{font-size:10px;font-weight:700;color:%s;letter-spacing:0.8px;text-transform:uppercase}' % p['label3'])
	a('#SectionTitle{font-size:10px;font-weight:700;color:%s;letter-spacing:1px}' % p['label3'])

	# Field labels
	a('#FieldLabel{font-size:10px;color:%s;font-weight:500}' % p['label3'])

	# Card value
	a('#CardTitle{font-size:11px;color:%s;font-weight:600}' % p['label3'])
	a('#CardValue{font-size:26px;color:%s;font-weight:700}' % p['label'])
	a('#CardSub{font-size:11px;color:%s}' % p['label3'])

	# Separator
	a('#RowSep{background:%s;max-height:1px;min-height:1px}' % p['sep'])

	# Buttons
	a('QPushButton{background:%s;color:%s;border:1px solid %s;border-radius:8px;padding:0 14px;font-size:12px;font-weight:500;min-height:32px}' % (p['ctrl_bg'], p['label2'], p['ctrl_border']))
	a('QPushButton:hover{background:%s}' % p['ctrl_hover'])
	a('QPushButton:pressed{background:%s}' % p['sep'])
	a('QPushButton:disabled{color:%s}' % p['label4'])
	a('QPushButton#Primary{background:%s;color:#FFFFFF;border:1px solid %s;font-weight:600}' % (p['accent'], p['accent']))
	a('QPushButton#Primary:hover{background:%s;border-color:%s}' % (p['accent_hover'], p['accent_hover']))
	a('QPushButton#Danger{background:%s;color:#FFFFFF;border:1px solid %s;font-weight:600}' % (p['red'], p['red']))
	a('QPushButton#Danger:hover{background:#C41E1E;border-color:#C41E1E}')
	a('QPushButton#Ghost{background:transparent;border:none;color:%s;padding:6px 10px}' % p['accent_text'])
	a('QPushButton#Ghost:hover{background:%s}' % p['accent_soft'])
	a('QPushButton#SmallButton{min-height:28px;padding:0 10px;font-size:11px}')
	a('QPushButton#RunButton{min-height:40px;font-size:14px;font-weight:600;padding:0 24px}')

	# Combo/Input
	a('QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox,QDateTimeEdit{background:%s;border:1px solid %s;border-radius:6px;padding:0 10px;color:%s;min-height:30px;font-size:12px}' % (p['ctrl_bg'], p['ctrl_border'], p['label']))
	a('QComboBox:hover,QLineEdit:hover,QSpinBox:hover,QDateTimeEdit:hover{border:1px solid %s}' % p['sep_strong'])
	a('QComboBox:focus,QLineEdit:focus,QSpinBox:focus,QDateTimeEdit:focus{border:1px solid %s}' % p['accent'])
	a('QComboBox::drop-down{border:none;width:20px}')
	a('QComboBox::down-arrow{image:none;border-left:3px solid transparent;border-right:3px solid transparent;border-top:4px solid %s;margin-right:6px}' % p['label3'])
	a('QComboBox QAbstractItemView{background:%s;border:1px solid %s;border-radius:8px;padding:4px;selection-background-color:%s;selection-color:%s;outline:none}' % (p['surface'], p['sep'], p['sel_bg'], p['sel_fg']))

	# Checkbox
	a('QCheckBox{spacing:6px;font-size:12px;background:transparent}')
	a('QCheckBox::indicator{width:16px;height:16px;border:1px solid %s;border-radius:4px;background:%s}' % (p['ctrl_border'], p['ctrl_bg']))
	a('QCheckBox::indicator:checked{background:%s;border-color:%s}' % (p['accent'], p['accent']))

	# Tables
	a('QTableWidget,QTreeWidget,QListWidget{background:%s;border:1px solid %s;border-radius:12px;gridline-color:%s;selection-background-color:%s;selection-color:%s;outline:none}' % (p['surface'], p['sep'], p['sep'], p['sel_bg'], p['sel_fg']))
	a('QHeaderView::section{background:%s;color:%s;border:none;border-bottom:1px solid %s;padding:10px 14px;font-weight:700;font-size:10px;letter-spacing:0.6px;text-transform:uppercase}' % (p['surface_alt'], p['label3'], p['sep']))
	a('QTableWidget::item{padding:10px 14px;border-bottom:1px solid %s}' % p['sep'])
	a('QTableWidget::item:selected{background:%s}' % p['sel_bg'])

	# ScrollArea
	a('QScrollArea{background:transparent;border:none}')
	a('QScrollArea > QWidget > QWidget{background:transparent}')
	a('QScrollBar:vertical{background:transparent;width:10px;margin:2px}')
	a('QScrollBar::handle:vertical{background:%s;border-radius:5px;min-height:30px}' % p['label4'])
	a('QScrollBar::handle:vertical:hover{background:%s}' % p['label3'])
	a('QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0}')
	a('QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:transparent}')
	a('QScrollBar:horizontal{background:transparent;height:10px;margin:2px}')
	a('QScrollBar::handle:horizontal{background:%s;border-radius:5px;min-width:30px}' % p['label4'])
	a('QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{width:0}')
	a('QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{background:transparent}')

	# Progress
	a('QProgressBar{background:%s;border:none;border-radius:4px;height:6px;text-align:center;color:%s;font-size:11px}' % (p['sep'], p['label3']))
	a('QProgressBar::chunk{background:%s;border-radius:4px}' % p['accent'])

	# StatusBar
	a('QStatusBar{background:%s;color:%s;border-top:1px solid %s;font-size:11px}' % (p['surface'], p['label3'], p['sep']))
	a('QStatusBar QLabel{padding:0 8px}')

	# Text/Log
	a('QTextEdit,QPlainTextEdit{background:%s;border:1px solid %s;border-radius:8px;padding:10px;color:%s;font-family:Consolas,monospace;font-size:11px}' % (p['surface_alt'], p['sep'], p['label2']))

	# TabWidget (for library)
	a('QTabWidget::pane{border:none;background:transparent}')
	a('QTabBar::tab{background:transparent;color:%s;padding:10px 16px;border-bottom:2px solid transparent;font-size:13px;margin-bottom:-1px;font-weight:500}' % p['label3'])
	a('QTabBar::tab:hover{color:%s}' % p['label2'])
	a('QTabBar::tab:selected{color:%s;border-bottom-color:%s;font-weight:600}' % (p['accent'], p['accent']))

	# Tooltip
	a('QToolTip{background:%s;color:%s;border:1px solid %s;padding:6px 10px;border-radius:6px;font-size:11px}' % (p['label'], p['surface'], p['label']))

	return chr(10).join(q)