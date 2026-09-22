import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import quality_gate as QG
v = 'output/CHECK/anime_mv_test.mp4'
q = QG.evaluate(v)
print(json.dumps(q, ensure_ascii=False, indent=2, default=str))