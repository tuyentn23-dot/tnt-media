import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import auto_youtube_bot_v2 as b
bot=b.AutoYouTubeV2.__new__(b.AutoYouTubeV2)
for i in range(3):
 p, h = bot.make_cat_video()
 print('made', p, h)
