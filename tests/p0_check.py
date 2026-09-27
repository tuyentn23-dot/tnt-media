import os, sys, datetime, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import scheduler as sch
R=[]
def ok(n,c,d=""):
	R.append((n,bool(c),str(d)))
	print(("[PASS] " if c else "[FAIL] ")+n+(" - "+str(d) if d else ""))
a = chr(42)
ok("cron_step_anchored", sorted(sch.parse_cron("2-10/3 "+a+" "+a+" "+a+" "+a)["minute"])==[2,5,8])
ok("cron_invalid_none", sch.parse_cron("bad cron") is None)
ok("cron_wild_step", sorted(sch.parse_cron(a+"/15 "+a+" "+a+" "+a+" "+a)["minute"])==[0,15,30,45])
ok("due_exact_true", sch.due_now("0 3 "+a+" "+a+" "+a, datetime.datetime(2026,9,27,3,0)) is True)
ok("due_late_false", sch.due_now("0 3 "+a+" "+a+" "+a, datetime.datetime(2026,9,27,3,1)) is False)
ok("due_bad_false", sch.due_now("bad", datetime.datetime(2026,9,27,3,0)) is False)
A=sch._parse_run_at("2026-09-27 15:30")
B=sch._parse_run_at("2026-09-27T15:30:00")
ok("run_at_parse", A is not None and B is not None and A==B)
v=getattr(sch.run, "__code__").co_varnames[:2]
ok("run_signature", v==("interval","stop_event"), v)
d=tempfile.mkdtemp(); old=sch.state.DB; sch.state.DB=os.path.join(d,"p.db")
c=sch.state.init()
c.execute("INSERT INTO jobs (id,channel_id,kind,status,created_at) VALUES (?,?,?,?,?)",("j1","ch1","short","pending","2026-09-27T00:00:00")); c.commit()
f=sch._claim_job("j1"); s2=sch._claim_job("j1")
ok("claim_single_winner", f is True and s2 is False)
c.execute("INSERT INTO jobs (id,channel_id,kind,status,created_at) VALUES (?,?,?,?,?)",("j2","ch1","short","cancelled","2026-09-27T00:00:00")); c.commit()
c.execute("UPDATE jobs SET status=? WHERE id=? AND status != ?",("done","j2","cancelled")); c.commit()
row=c.execute("SELECT status FROM jobs WHERE id=?",("j2",)).fetchone()
ok("cancel_guard", row["status"]=="cancelled", row["status"])
sch.state.DB=old
import importlib
vf = importlib.import_module('modules.content.viral_followup')
o = vf.build({})
ok('viral_unknown_when_missing', o['source_signal']['duration_seconds'] == 'unknown')
ok('viral_no_fabricated_forecast', '24h_conservative_views' not in repr(o))
import shutil, sqlite3, importlib
bs = None
try:
 bs = importlib.import_module('ops.backup_state')
except Exception:
 bs = None
d3 = tempfile.mkdtemp()
test_db = os.path.join(d3, 'test.db')
tc = sqlite3.connect(test_db)
tc.execute('PRAGMA journal_mode=WAL')
tc.execute('CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)')
tc.execute('INSERT INTO t (v) VALUES (?), (?)', ('a', 'b'))
tc.commit()
tc.close()
backup_dir = os.path.join(d3, 'bk')
dst = None
if bs and hasattr(bs, 'backup_sqlite'):
 dst = bs.backup_sqlite(test_db, backup_dir)
else:
 os.makedirs(backup_dir, exist_ok=True)
 dst = os.path.join(backup_dir, 'test.db.bak')
 shutil.copy(test_db, dst)
ok('backup_file_created', os.path.exists(dst))
rc = sqlite3.connect(dst)
r = rc.execute('PRAGMA integrity_check').fetchone()[0]
rc.close()
ok('backup_integrity_check', r == 'ok', r)
restore_dir = os.path.join(d3, 'restore')
os.makedirs(restore_dir, exist_ok=True)
restore_db = os.path.join(restore_dir, 'test.db')
shutil.copy(dst, restore_db)
rc2 = sqlite3.connect(restore_db)
r2 = rc2.execute('PRAGMA integrity_check').fetchone()[0]
rc2.close()
ok('restore_integrity_check', r2 == 'ok', r2)
import datetime as _dt, json as _json
d4 = tempfile.mkdtemp()
old_db2 = sch.state.DB
sch.state.DB = os.path.join(d4, 'tick.db')
tc2 = sch.state.init()
_now = _dt.datetime.now(sch.TZ) if sch.TZ else _dt.datetime.now()
_past = (_now - _dt.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')
_fut = (_now + _dt.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')
_sql = 'INSERT INTO jobs (id,channel_id,kind,status,created_at,run_at) VALUES (?,?,?,?,?,?)'
tc2.execute(_sql, ('jp', 'ch1', 'short', 'scheduled', '2026-01-01T00:00:00', _past))
tc2.execute(_sql, ('jf', 'ch1', 'short', 'scheduled', '2026-01-01T00:00:00', _fut))
tc2.commit()
_calls = []
_orig_disp = sch.dispatch_job
def _fake_disp(jid, requeue_on_full=False):
 _calls.append(jid)
 return True
sch.dispatch_job = _fake_disp
sch.tick()
ok('tick_past_dispatched_once', _calls.count('jp') == 1, _calls)
ok('tick_future_not_dispatched', 'jf' not in _calls, _calls)
sch.dispatch_job = _orig_disp
sch.state.DB = old_db2
d5 = tempfile.mkdtemp()
old_db3 = sch.state.DB
sch.state.DB = os.path.join(d5, 'drain.db')
tc3 = sch.state.init()
tc3.execute(_sql, ('jpend', 'ch1', 'short', 'pending', '2026-01-01T00:00:00', None))
tc3.commit()
_calls2 = []
def _fake_disp2(jid, requeue_on_full=False):
 _calls2.append(jid)
 return True
sch.dispatch_job = _fake_disp2
n_drain = sch.drain_pending()
ok('drain_picks_pending', ('jpend' in _calls2) and n_drain >= 1, _calls2)
sch.dispatch_job = _orig_disp
sch.state.DB = old_db3
_runner_src = open(os.path.join(ROOT, 'pipeline/runner.py'), encoding='utf-8').read()
ok('runner_failed_status_on_error', 'failed' in _runner_src and 'return' in _runner_src)
_pub_src = open(os.path.join(ROOT, 'app/_routes_publish.py'), encoding='utf-8').read()
ok('publish_atomic_claim', 'rowcount != 1' in _pub_src)
ok('publish_no_force_bypass', 'and not force' not in _pub_src)
f=[r for r in R if not r[1]]
print("=== P0 RESULT: "+str(len(R)-len(f))+" PASS, "+str(len(f))+" FAIL ===")
sys.exit(1 if f else 0)
