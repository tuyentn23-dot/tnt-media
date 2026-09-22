import sys, os
sys.path.insert(0, '.')
import auto_youtube_bot_v3 as b
bot = b.AutoYouTubeV3.__new__(b.AutoYouTubeV3)
p, h = bot.make_video()
print('OK', p, os.path.getsize(p))
