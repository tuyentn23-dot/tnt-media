import sys, os
sys.path.insert(0, '.')
import auto_youtube_bot_v4 as b
bot = b.AutoYouTubeV4.__new__(b.AutoYouTubeV4)
p, t, h = bot.make_video()
print('OK', t, os.path.getsize(p))
