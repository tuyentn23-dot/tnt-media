import os, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import anime_ai_render as AR
imgs = [
	'output/ai_anime/flux_pose0.jpg',
	'output/ai_anime/expr0.jpg',
	'output/ai_anime/flux_pose1.jpg',
	'output/ai_anime/expr1.jpg',
	'output/ai_anime/flux_pose2.jpg',
	'output/ai_anime/expr2.jpg',
	'output/ai_anime/flux_pose3.jpg',
]
out = os.path.abspath('output/CHECK/anime_mv_test.mp4')
os.makedirs(os.path.dirname(out), exist_ok=True)
t0 = time.time()
AR.make_mv(imgs, out, dur=14.0, fps=8)
print('elapsed', round(time.time() - t0, 1))
print('size', os.path.getsize(out))