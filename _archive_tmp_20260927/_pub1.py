import os, sys, importlib, time
sys.path.insert(0, os.getcwd())
U = chr(95)
f = 'output/chMialinhcute' + U + 'live' + U + 'cute' + U + 'animals' + U + 'e9e04e4b9c' + U + '20260926' + U + '130442.mp4'
op = importlib.import_module('ops.os' + U + 'publish')
op_set = getattr(op, 'set' + U + 'channel')
op_pub = getattr(op, 'publish')
op_set('Mialinhcute')
res = op_pub(f, 'Axolotl co the tai sinh nao khong?', description='', tags=None, privacy='public', topic='cute' + U + 'animals' + U + time.strftime('%Y%m%d%H%M%S'))
print('RESULT:', res)
