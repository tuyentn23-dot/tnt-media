import json
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

CHANNEL_ID = "UCbblZzHm3CZzmoUZznfIoTg"
FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=
" + CHANNEL_ID

response = requests.get(
 FEED_URL,
 headers={"User-Agent": "Mozilla/5.0