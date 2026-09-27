# -- coding: utf-8 --
# ops/_no_window.py - An cua so console khi spawn subprocess (Windows)
# Import module nay de monkeypatch subprocess.Popen toan cuc.
import subprocess, sys
if sys.platform == 'win32':
	_CNW = 0x08000000
	_orig_popen = subprocess.Popen
	class _NWPopen(_orig_popen):
		def init(self, args, **kwargs):
			cf = kwargs.get('creationflags', 0)
			kwargs['creationflags'] = cf | _CNW
			if 'startupinfo' not in kwargs:
				si = subprocess.STARTUPINFO()
				si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				si.wShowWindow = subprocess.SW_HIDE
				kwargs['startupinfo'] = si
			super().init(args, **kwargs)
	def _si():
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		si.wShowWindow = subprocess.SW_HIDE
		return si
	def patch():
		subprocess.Popen = _NWPopen
		return True
	def popen_kwargs():
		return {'creationflags': _CNW, 'startupinfo': _si()}
	patch()
else:
	def patch():
		return False
	def popen_kwargs():
		return {}
	def _si():
		return None