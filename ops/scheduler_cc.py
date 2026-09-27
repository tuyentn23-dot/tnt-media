import os, json, time, threading
from pathlib import Path
from croniter import croniter
from datetime import datetime
from ops.pipeline_cc import run_channel

ROOT = Path(file).resolve().parent.parent


def load_channels():
 return json.loads((ROOT / 'config' / 'channels.json').read_text(encoding='utf-8'))['channels']


def run_one(ch):
 try:
 r = run_channel(ch)
 print('[scheduler]', ch['name'], r, flush=True)
 except Exception as e:
 print('[scheduler][ERR]', ch['name'], repr(e), flush=True)


def job_all():
 for ch in load_channels():
 run_one(ch)


def _next_run(cron_expr, base=None):
 base = base or datetime.now()
 return croniter(cron_expr, base).get_next(datetime)


def main(run_now=True):
 if run_now:
 job_all()
 # per-channel cron loop
 chans = load_channels()
 schedule_map = {}
 for ch in chans:
 expr = ch.get('cron', '0 */6 * * *')
 schedule_map[ch['name']] = {
 'ch': ch,
 'cron': expr,
 'next': _next_run(expr),
 }
 while True:
 now = datetime.now()
 for name, s in list(schedule_map.items()):
 if now >= s['next']:
 run_one(s['ch'])
 s['next'] = _next_run(s['cron'], now)
 print(f"[scheduler] {name} next run at {s['next']}