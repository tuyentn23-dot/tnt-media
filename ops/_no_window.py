# -- coding: utf-8 --
# ops/_no_window.py - An cua so console khi spawn subprocess (Windows)
# Patch toan cuc: subprocess.Popen + os.system + os.popen (cac ham khac deu route qua Popen).
import subprocess, sys, os
_CNW = 0x08000000 # CREATE_NO_WINDOW
_orig_popen = subprocess.Popen
_orig_system = os.system
_orig_popen_os = os.popen
def _si():
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	si.wShowWindow = subprocess.SW_HIDE
	return si
class _NWPopen(_orig_popen):
	def init(self, args, **kwargs):
		if sys.platform == 'win32':
			cf = kwargs.get('creationflags', 0)
			kwargs['creationflags'] = cf | _CNW
			if 'startupinfo' not in kwargs:
				kwargs['startupinfo'] = _si()
		super().init(args, **kwargs)
def _hidden_system(cmd):
	if sys.platform != 'win32':
		return _orig_system(cmd)
	try:
		p = _orig_popen(cmd, shell=True, creationflags=_CNW, startupinfo=_si())
		return p.wait()
	except Exception:
		return _orig_system(cmd)
def _hidden_ospopen(cmd, mode='r', bufsize=-1):
	if sys.platform != 'win32':
		return _orig_popen_os(cmd, mode, bufsize)
	p = _orig_popen(cmd, shell=True, stdout=subprocess.PIPE, creationflags=_CNW, startupinfo=_si())
	return p.stdout
def patch():
	subprocess.Popen = _NWPopen
	os.system = _hidden_system
	os.popen = _hidden_ospopen
	return True
def popen_kwargs():
	return {'creationflags': _CNW, 'startupinfo': _si()}
def run(cmd, **kw):
	k = {'creationflags': _CNW, 'startupinfo': _si()}
	k.update(kw)
	return _orig_popen(cmd, **k)
patch()