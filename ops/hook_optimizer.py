# hook_optimizer.py - chon hook toi uu dua tren data that (tab)
import os, sys, json
sys.path.insert(0, os.getcwd())
from ops import hook_engine as HE
from ops import viral_hook as VH

def best_hook(item, n=5):
	topic = item.get('topic', '')
	name = item.get('name') or topic
	base = item.get('hook', '')
	cands = [base] + HE.top_hooks(topic, name) + VH.fill(topic, name)
	seen = []
	for c in cands:
		if c and c not in seen:
			seen.append(c)
	ranked = sorted(seen, key=lambda h: HE.score(h), reverse=True)
	return ranked[:n]
