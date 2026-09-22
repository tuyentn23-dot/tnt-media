# -- coding: utf-8 --
"""evolution - YC6: evolution loop 3 cap (A/B prompt, weight tuning, tool gen+approve)."""
import os, sys, json, sqlite3, hashlib
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
if not os.path.isdir(os.path.join(ROOT, 'ops')):
	ROOT = os.getcwd()
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, 'system', 'state.db')
GEN = os.path.join(ROOT, 'memory', 'gen_tools')
def now(): return datetime.now().isoformat(timespec='seconds')

def tier1_ab_prompt(top_n=3):
	con = sqlite3.connect(DB)
	con.row_factory = sqlite3.Row
	prompts = list(con.execute('SELECT id, channelId, topic, format FROM decisions ORDER BY id DESC LIMIT ?', (top_n,)))
	out = []
	for p in prompts:
		variants = json.dumps([dict(id='A'), dict(id='B')])
		name = 'ab_' + str(p['id'])
		exists = con.execute('SELECT id FROM experiments WHERE name=?', (name,)).fetchone()
		if not exists:
			con.execute('INSERT INTO experiments (name, variantsJson, metric, winner, samples, createdAt) VALUES (?,?,?,?,?,?)', (name, variants, 'views', None, 0, now()))
		out.append(name)
	con.commit()
	con.close()
	return dict(tier=1, ab_experiments=out)

def tier2_weights():
	from ops import weights_tuner as WT
	r = WT.tune()
	return dict(tier=2, ok=r.get('ok'), topics=len(r.get('topic_weights', {})), formats=len(r.get('format_weights', {})))

def tier3_tool_gen(approve=True):
	os.makedirs(GEN, exist_ok=True)
	con = sqlite3.connect(DB)
	missing = [r[0] for r in con.execute('SELECT name FROM tools WHERE health=?', ('unknown',))]
	gen = []
	if missing:
		name = 'gen_' + hashlib.md5((missing[0] + now()).encode()).hexdigest()[:8]
		path = os.path.join(GEN, name + '.py')
		if not os.path.exists(path):
			open(path, 'w', encoding='utf-8').write('# auto-generated tool stub' + chr(10) + 'def run(): return dict(ok=True)' + chr(10))
		rel = os.path.relpath(path, ROOT)
		if approve:
			con.execute('INSERT OR IGNORE INTO tools (name, path, version, description, health, createdAt, updatedAt) VALUES (?,?,?,?,?,?,?)', (name, rel, '1', 'auto-gen candidate', 'pending', now(), now()))
		gen.append(dict(name=name, path=rel))
	con.commit()
	con.close()
	return dict(tier=3, generated=gen)

def run_once():
	r1 = tier1_ab_prompt()
	r2 = tier2_weights()
	r3 = tier3_tool_gen(approve=True)
	res = dict(ok=True, at=now(), tiers=[r1, r2, r3])
	open(os.path.join(ROOT, 'memory', 'evolution_state.json'), 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False, indent=1))
	return res

if os.path.basename(sys.argv[0]).startswith('evolution'):
	print(json.dumps(run_once(), ensure_ascii=True, indent=1))
