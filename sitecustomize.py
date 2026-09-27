# -- coding: utf-8 --
# sitecustomize.py - Python tu dong import file nay khi khoi dong (neu ROOT tren sys.path).
# Muc dich: patch subprocess/os de KHONG hien cua so console tren Windows,
# ap dung cho MOI tien trinh python/pythonw chay tu workspace nay.
import os, sys
if sys.platform == 'win32':
	try:
		_root = os.path.dirname(os.path.abspath(file))
		if _root not in sys.path:
			sys.path.insert(0, _root)
		from ops import _no_window # noqa: F401 (side-effect: patch Popen/os.system/os.popen)
	except Exception:
		pass