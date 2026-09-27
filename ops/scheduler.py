import os
import sys
import time
try:
	import schedule
except ImportError:
	print("[WARNING] schedule lib missing; pip install schedule")
	schedule = None


def job():
	print("=" * 50)
	print("AUTO-PUBLISH SCHEDULER TICK")
	print("=" * 50)
	os.system("python ops/autopublish.py")


def main():
	if schedule is None:
		print("[WARNING] schedule lib missing")
		return
	once = "--once" in sys.argv
	schedule.every(10).minutes.do(job)
	print("[scheduler] started, running job once now...")
	job()
	if once:
		print("[scheduler] once mode done")
		return
	while True:
		schedule.run_pending()
		time.sleep(60)


if name == "main":
	main()
