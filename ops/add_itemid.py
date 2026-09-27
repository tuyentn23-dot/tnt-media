p = 'pipeline/runner.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
T2 = T + T
T3 = T2 + T
Q = chr(39)
# 1. Doi signature run_job de nhan item_id
old_sig = 'def run_job(job, dry_run=False):'
new_sig = 'def run_job(job, dry_run=False, item_id=None):'
if old_sig in src:
	src = src.replace(old_sig, new_sig, 1)
	print('changed sig')
else:
	print('sig not found')
# 2. Chen logic chon item_id truoc 'item = fresh[0]'
old_pick = T3 + 'item = fresh[0]'
new_pick = (T3 + 'if item_id:' + NL
	+ T3*2 + 'items_all = ch.load_content(job.channel_id, kind)' + NL
	+ T3*2 + 'matches = [x for x in items_all if x.get(' + Q + 'id' + Q + ') == item_id]' + NL
	+ T3*2 + 'if matches:' + NL
	+ T3*3 + 'item = matches[0]' + NL
	+ T3*2 + 'else:' + NL
	+ T3*3 + 'item = fresh[0]' + NL
	+ T3 + 'else:' + NL
	+ T3*2 + 'item = fresh[0]')
if old_pick in src:
	src = src.replace(old_pick, new_pick, 1)
	print('patched pick')
else:
	print('pick not found')
# 3. Them arg --item-id
old_arg = "ap.add_argument('--kind', type=str, default=None)"
new_arg = old_arg + NL + T + "ap.add_argument('--item-id', type=str, default=None)"
if old_arg in src:
	src = src.replace(old_arg, new_arg, 1)
	print('added arg')
# 4. Truyen item_id vao run_job
old_call = 'r = run_job(j, dry_run=args.dry_run)'
new_call = 'r = run_job(j, dry_run=args.dry_run, item_id=getattr(args, ' + Q + 'item_id' + Q + ', None))'
if old_call in src:
	src = src.replace(old_call, new_call, 1)
	print('patched call')
open(p, 'w', encoding='utf-8', newline='').write(src)
print('done')
