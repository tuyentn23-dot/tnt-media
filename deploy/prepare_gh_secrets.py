# prepare_gh_secrets.py
import base64, os

FILES = [
 ('TOKEN_PICKLE_B64', 'config/token.pickle'),
 ('TOKEN_NEW_CHANNEL_B64', 'memory/token_new_channel.json'),
 ('CLIENT_SECRETS_JSON_B64', 'config/client_secrets.json'),
 ('TOKEN_MIALINHCUTE_B64', 'channels/Mialinhcute/token.pickle'),
]

def enc(path):
 return base64.b64encode(open(path, 'rb').read()).decode() if os.path.exists(path) else 'MISSING'

rows = [(name, path, enc(path)) for name, path in FILES]
lines = ['='*60 + chr(10) + name + ' ' + path + ' ' + b64 for name, path, b64 in rows]
print(chr(10).join(lines))
