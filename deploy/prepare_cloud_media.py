# -- coding: utf-8 --
"""prepare_cloud_media - tao cloud_media/ gon (subset library + music) de deploy cloud."""
import os, sys, json, shutil, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
if not os.path.isdir(os.path.join(ROOT, 'ops')):
	ROOT = os.getcwd()
DEST = os.path.join(ROOT, 'cloud_media')
KEEP = 3
MAX_MB = 25

def topics_needed():
	need = set()
	for cid in ['Mialinhcute', 'vilevi5676']:
		p = os.path.join(ROOT, 'channels', cid, 'content_db.json')
		if os.path.exists(p):
			need.update(json.load(open(p, encoding='utf-8')).keys())
	return need

def copy_subset(src, dst, keep, max_bytes):
	if not os.path.isdir(src):
		return 0
	files = [f for f in os.listdir(src) if f.lower().endswith(('.mp4', '.wav', '.mp3'))]
	files = [f for f in files if os.path.getsize(os.path.join(src, f)) <= max_bytes]
	random.seed(42)
	random.shuffle(files)
	os.makedirs(dst, exist_ok=True)
	n = 0
	for f in files[:keep]:
		shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
		n += 1
	return n

def main():
	need = topics_needed()
	print('topics:', sorted(need))
	max_bytes = MAX_MB * 1024 * 1024
	total = 0
	for topic in need:
		src = os.path.join(ROOT, 'library', topic)
		dst = os.path.join(DEST, 'library', topic)
		n = copy_subset(src, dst, KEEP, max_bytes)
		if n:
			print(' ', topic, n)
		total += n
	msrc = os.path.join(ROOT, 'music_bank')
	mdst = os.path.join(DEST, 'music_bank')
	m = copy_subset(msrc, mdst, 10, max_bytes)
	print('music:', m)
	print('DONE total clips:', total)

if os.path.basename(sys.argv[0]).startswith('prepare_cloud_media'):
	main()
