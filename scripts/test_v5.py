import sys, os
sys.path.insert(0, '.')
import auto_youtube_bot_v5 as b
bot = b.AutoYouTubeV5.__new__(b.AutoYouTubeV5)
p, t, h = bot.make_video()
print('OK', t, os.path.getsize(p))
