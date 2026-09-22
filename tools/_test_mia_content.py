import sys
sys.path.insert(0,'.')
from ops import mia_content as mc
for k in mc.NEW_TOPIC_SOURCES:
    print(k, 'fresh_items=', len(mc.fresh_items(k)), 'next_topic=', mc.next_topic(k))
