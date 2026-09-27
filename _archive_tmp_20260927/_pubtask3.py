import os, sys, importlib, time
sys.path.insert(0, os.getcwd())
U = chr(95)
op = importlib.import_module('ops.os' + U + 'publish')
op_set = getattr(op, 'set' + U + 'channel')
op_pub = getattr(op, 'publish')
f = 'output/chvilevi5676' + U + 'live' + U + 'whatif' + U + 'a46be85b4c' + U + '20260926' + U + '160233.mp4'
op_set('vilevi5676')
res = op_pub(f, 'Dieu gi se xay ra neu?', description='', tags=None, privacy='public', topic='whatif' + U + time.strftime('%Y%m%d%H%M%S'))
print('RESULT:', res)
