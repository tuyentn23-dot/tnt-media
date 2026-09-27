# -- coding: utf-8 --
# ops/_no_window.py - An console window khi spawn subprocess (Windows)
import subprocess, sys
if sys.platform == 'win32':
	_CNW = 0x08000000
	_orig_popen = subprocess.Popen
	class _NWPopen(_orig_popen):
		def __init__(self, *args, **kwargs):
			cf = kwargs.get('creationflags', 0)
			kwargs['creationflags'] = cf | _CNW
			if 'startupinfo' not in kwargs:
				si = subprocess.STARTUPINFO()
				si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				si.wShowWindow = 0
				kwargs['startupinfo'] = si
			super().__init__(*args, **kwargs)
	subprocess.Popen = _NWPopen
	_orig_run = subprocess.run
	def _nw_run(*args, **kwargs):
		cf = kwargs.get('creationflags', 0)
		kwargs['creationflags'] = cf | _CNW
		return _orig_run(*args, **kwargs)
	subprocess.run = _nw_run
