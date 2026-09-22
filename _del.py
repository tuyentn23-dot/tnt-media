import sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
def dele(yt, vid):
	try:
		yt.videos().delete(id=vid).execute()
		return vid + ' DELETED'
	except Exception as e:
		return vid + ' FAIL ' + str(e)[:60]
for ch, ids in [('Mialinhcute', ['-nXf2g39vSA', '-eF0lyWaYBA', 'LbB_ANpQE10', '_SnLdSiFmm4', 'J8DVEvNSahg']), ('vilevi5676', ['0pvu_ilZGSk', 'EoI-f_1PuJ8', 'yJ3-2XMLivc', 'oTCLm5tymXA', 'Yu5Ccmsjos8'])]:
	OP.set_channel(ch)
	yt = OP.load_yt()
	for vid in ids:
		print(ch, dele(yt, vid))
