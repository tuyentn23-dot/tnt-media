# -- coding: utf-8 --
# ops/_no_window.py - An cua so console khi spawn subprocess (Windows)
# Import module nay de monkeypatch subprocess.Popen + os.system toan cuc.
import subprocess, sys, os
if sys.platform == 'win32':
	_CNW = 0x08000000
	_orig_popen = subprocess.Popen
	_orig_system = os.system
	def _si():
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		si.wShowWindow = subprocess.SW_HIDE
		return si
	class _NWPopen(_orig_popen):
		def init(self, args, **kwargs):
			cf = kwargs.get('creationflags', 0)
			kwargs['creationflags'] = cf | _CNW
			if 'startupinfo' not in kwargs:
				kwargs['startupinfo'] = _si()
			super().init(args, **kwargs)
	def _hidden_system(cmd):
		try:
			return _orig_popen(cmd, shell=True, creationflags=_CNW, startupinfo=_si()).wait()
		except Exception:
			return _orig_system(cmd)
	def patch():
		subprocess.Popen = _NWPopen
		os.system = _hidden_system
		return True
	def popen_kwargs():
		return {'creationflags': _CNW, 'startupinfo': _si()}
	def run(cmd, **kw):
		k = {'creationflags': _CNW, 'startupinfo': _si()}
		k.update(kw)
		return _orig_popen(cmd, **k)
	patch()
else:
	def patch():
		return False
	def popen_kwargs():
		return {}
	def _si():
		return None
	def run(cmd, **kw):
		return subprocess.run(cmd, **kw)