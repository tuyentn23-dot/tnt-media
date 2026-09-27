"""Dump all channel-related memory files to find the REAL channel setup."""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(file)))
os.chdir(ROOT)

FILES = [
 'memory/channel_registry.json',
 'memory/channels.json',
 'memory/channels_config.json',
 'memory/channel_real.json',
 'memory/channel_memory.json',
 'memory/multichannel_state.json',
 'memory/token.json',
 'memory/token_channel_01.json',
 'config/channels.json',
]

out = {}
for p in FILES:
 if os.path.exists(p):
 try:
 out[p] = json.load(open(p, encoding='utf-8'))
 except Exception as e:
 out[p] = 'PARSE_ERR: ' + str(e)
 else:
 out[p] = 'MISSING'

with open('memory/_channels_audit.json', 'w', encoding='utf-8') as f:
 json.dump(out, f, ensure_ascii=False, indent=2)

for p, v in out.items():
 print('=' * 60)
 print(p)
 print('=' * 60)
 if isinstance(v, (dict, list)):
 print(json.dumps(v, ensure_ascii=False, indent=2)[:700])
 else:
 print(v)
 print()
