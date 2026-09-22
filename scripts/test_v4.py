import sys, os
sys.path.insert(0, '.')
import auto_youtube_bot_v4 as b
bot = b.AutoYouTubeV4.__new__(b.AutoYouTubeV4)
for i in range(3):
 p, topic, hook = bot.make_video()
 print('OK', topic, os.path.getsize(p), p)
