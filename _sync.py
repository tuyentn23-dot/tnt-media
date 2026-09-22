import sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
from ops.analytics_manager import AnalyticsManager
OP.set_channel('Mialinhcute')
yt = OP.load_yt()
am = AnalyticsManager()
am.sync_youtube_metrics(yt)
print('SYNC DONE')
