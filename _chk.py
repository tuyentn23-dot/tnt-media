import sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
def chk(ch):
	try:
		OP.set_channel(ch)
		tp = OP._resolve_token_path()
		return (ch, str(tp))
	except Exception as e:
		return (ch, 'ERR ' + str(e)[:80])
for ch in ['Mialinhcute', 'whatif_vi', 'vilevi5676']:
	print(chk(ch))
