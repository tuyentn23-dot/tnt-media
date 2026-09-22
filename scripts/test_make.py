import sys, os
sys.path.insert(0, '.')
import auto_youtube_bot_v2 as b
bot = b.AutoYouTubeV2.__new__(b.AutoYouTubeV2)
p, h = bot.make_cat_video()
print('OK:', p)
print('SIZE:', os.path.getsize(p))
