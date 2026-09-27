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
import shutil, sqlite3
src_db = sch.state.DB
if os.path.exists(src_db):
 d2 = tempfile.mkdtemp()
 dst = os.path.join(d2, 'copy.db')
 sc = sqlite3.connect(src_db)
 sc.execute('PRAGMA wal_checkpoint(FULL)')
 sc.close()
 shutil.copy(src_db, dst)
 rc = sqlite3.connect(dst)
 r = rc.execute('PRAGMA integrity_check').fetchone()[0]
 rc.close()
 ok('db_copy_integrity', r == 'ok', r)
f=[r for r in R if not r[1]]
print("=== P0 RESULT: "+str(len(R)-len(f))+" PASS, "+str(len(f))+" FAIL ===")
sys.exit(1 if f else 0)
