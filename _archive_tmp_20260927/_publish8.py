import os, sys, importlib, time, glob
sys.path.insert(0, os.getcwd())
U = chr(95)
op = importlib.import_module('ops.os' + U + 'publish')
op_set = getattr(op, 'set' + U + 'channel')
op_pub = getattr(op, 'publish')
files = open('logs/' + U + 'today' + U + 'videos.txt').read().strip().split(chr(10))
TITLES = {
	'anime': 'Goku manh den muc nao?',
	'roblox': 'Dao huyen thoai trong MM2 o dau ra?',
	'cute_animals': 'Axolotl co the tai sinh nao khong?',
	'gacha': 'Gacha love story',
	'facts': 'Su that thu vi ban chua biet',
	'food': 'Am thuc Viet Nam dac sac',
	'animals': 'Dong vat ky thu',
	'whatif': 'Dieu gi se xay ra neu?',
}
for f in files:
	if not f.strip():
		continue
	cid = 'Mialinhcute' if 'chMialinhcute' in f else 'vilevi5676'
	kind = 'unknown'
	for k in TITLES:
		if U + k + U in f:
			kind = k
			break
	title = TITLES.get(kind, 'Video')
	topic = 'batch' + U + time.strftime('%Y%m%d%H%M%S')
	print('===', cid, kind, os.path.basename(f)[:60], flush=True)
	op_set(cid)
	try:
		res = op_pub(f, title, description='', tags=None, privacy='public', topic=topic)
		print('RESULT:', res, flush=True)
	except Exception as e:
		print('ERR:', str(e)[:200], flush=True)
	time.sleep(3)
print('PUBLISH ALL DONE', flush=True)
