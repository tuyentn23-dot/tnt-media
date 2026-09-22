# quality_gate_vile.py - QG cho kenh ViLe Vi (video dai, max 180s)
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import viral_engine as VE
MAX_DUR = 90
MIN_SCORE = 65
MIN_HOOK = 2.0
def evaluate(video_path):
	if not os.path.exists(video_path):
		return {"ok": False, "passes": False, "score": 0, "reasons": ["file not found"]}
	try:
		m = VE.analyze(video_path)
	except Exception as e:
		return {"ok": False, "passes": False, "score": 0, "reasons": [str(e)[:100]]}
	dur = m.get("duration", 0)
	hook = m.get("hook_motion", 0)
	score = 0
	if dur <= MAX_DUR:
		score += 40
	if hook > MIN_HOOK:
		score += 30
	if dur >= 10:
		score += 30
	reasons = []
	if score < MIN_SCORE:
		reasons.append("score " + str(score) + " < " + str(MIN_SCORE))
	passes = score >= MIN_SCORE
	return {"ok": True, "passes": passes, "score": score, "metrics": m, "reasons": reasons}