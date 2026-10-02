# -- coding: utf-8 --
# ops/init.py - Ap patch an cua so console cho moi import ops
try:
	from ops import _no_window # noqa: F401 (side-effect: patch subprocess.Popen + os.system)
except Exception:
	pass
