# SCHEDULER & RECOVERY - CON LO HONG

## 3.1. Scheduler chi ho tro phut/gio

File: pipeline/scheduler.py
Van de:
- parse_cron chi expand minute + hour, bo qua day/month/weekday
- Khong ho tro */5 syntax
- Khong xu ly run_at (job dat gio)

Bang chung: Ham parse_cron(expr):
python
def parse_cron(expr):
 p = (expr or '').split()
 if len(p) != 5:
 return None
 out = { 'minute': set(), 'hour': set() }
 def expand(field, lo, hi):
 if field == '*': return set(range(lo, hi+1))
 s = set()
 for part in field.split(','):
 if '-' in part:
 a, b = part.split('-', 1)
 s.update(range(int(a), int(b)+1))
 else:
 s.add(int(part))
 return s
 out['minute'] = expand(p[0], 0, 59)
 out['hour'] = expand(p[1], 0, 23)
 return out


Sua: Dung croniter (pip) hoac tu viet day du:
- Expand ca 5 truong (minute, hour, day, month, weekday)
- Ho tro */n
- Ho tro danh sach, khoang, buoc

Xu ly run_at:
python
def tick():
 # ... xu ly cron ...
 # Them: xu ly job co run_at <= now va status='pending' -> dispatch
 rows = c.execute("SELECT id FROM jobs WHERE status='pending' AND run_at IS NOT NULL AND run_at <= ?", (state.now(),)).fetchall()
 for r in rows:
 dispatch_job(r['id'])


## 3.2. Recovery khong co heartbeat

File: pipeline/recovery.py
Van de:
- Danh dau job > 15 phut la failed dua vao updated_at
- Video render lau co the bi danh failed sai

Sua:
Them heartbeat: runner cap nhat jobs.updated_at moi 60s:
python
# Trong run_job, spawn thread heartbeat
def _hb():
 import threading, time
 c2 = state.init()
 while not stop_flag.is_set():
 c2.execute('UPDATE jobs SET updated_at=? WHERE id=?', (state.now(), job.job_id))
 c2.commit()
 time.sleep(60)

Recovery dua vao updated_at nay (moi 60s) -> nguong 15 phut la an toan.

## 3.3. Runner chua ap dung day du tham so

File: pipeline/runner.py
Van de: count, voice_override, length_override duoc truyen nhung chua ro co ap dung khong
Kiem tra can lam:
- Neu count=5 -> render 5 video (vong lap)
- voice_override='male_north' -> truyen vao style.voice
- length_override=90 -> cat/ghep video theo thoi luong do

Sua: Doc va ap dung tung tham so, viet test kiem tra.
