import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(file))))
from dotenv import load_dotenv
load_dotenv()

from ops.pipeline_cc import run_channel

chans = [
 {'name': 'vilevi', 'niche': 'life hacks', 'language': 'vi', 'token': 'memory/token_new_channel.json'},
 {'name': 'tnt_daily', 'niche': 'motivation', 'language': 'vi', 'token': 'config/token.pickle'},
]

for ch in chans:
 r = run_channel(ch, dry=True)
 print('DRYRUN', ch['name'], '=>', r, flush=True)
