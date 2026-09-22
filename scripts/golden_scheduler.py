import sys, os, time, datetime, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auto_youtube_bot_v2 as b
GOLDEN = [(18,0), (20,0)]
def next_golden():
	now = datetime.datetime.now()
	for h, m in GOLDEN:
		t = now.replace(hour=h, minute=m, second=0, microsecond=0)
		if t > now:
			return t
	return (now + datetime.timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
bot = b.AutoYouTubeV2()
while True:
	t = next_golden()
	wait = (t - datetime.datetime.now()).total_seconds()
	print('Cho den', t, 'con', int(wait//60), 'phut')
	if wait > 0:
		time.sleep(min(wait, 3600))
		if (t - datetime.datetime.now()).total_seconds() > 60:
			continue
	p, h = bot.make_cat_video()
	vid = bot.upload(p)
	print('DANG LUC GIO VANG:', vid)
	time.sleep(60)
