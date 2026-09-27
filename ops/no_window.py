# -- coding: utf-8 --
# ops/no_window.py - Shim tuong thich: chuyen tiep sang _no_window
# Mot so file cu import from ops import no_window.
from ops._no_window import * # noqa
from ops import _no_window as _nw
patch = _nw.patch
popen_kwargs = _nw.popen_kwargs
