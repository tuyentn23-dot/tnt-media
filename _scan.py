import sys, os, glob, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
def scan(f):
	try:
		return 'whatif_vi' in open(f, encoding='utf-8').read()
	except Exception:
		return False
files = glob.glob('memory/.json') + glob.glob('config/.json')
refs = [f for f in files if scan(f)]
print('refs', refs)
