import io, os, json, shutil
src = 'memory/content_db.json'
dst = 'channels/whatif_vi/content_db.json'
if os.path.exists(src):
	shutil.copyfile(src, dst)
	d = json.load(io.open(dst, encoding='utf-8'))
	print('MIGRATED content_db: kinds=', list(d.keys()))
	for k in d:
		print(' ', k, '=', len(d[k]), 'items')
else:
	print('NOT FOUND', src)
# migrate ledger
lsrc = 'memory/published_ledger.json'
ldst = 'channels/whatif_vi/published_ledger.json'
if os.path.exists(lsrc):
	shutil.copyfile(lsrc, ldst)
	l = json.load(io.open(ldst, encoding='utf-8'))
	print('MIGRATED ledger: signatures=', len(l.get('signatures', {})))
# copy token
for cand in ['config/token.pickle']:
	if os.path.exists(cand):
		shutil.copyfile(cand, 'channels/whatif_vi/token.pickle')
		print('COPIED token ->', 'channels/whatif_vi/token.pickle')
		break
else:
	print('NO token found at config/token.pickle')
