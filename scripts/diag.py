import os, shutil, importlib

print('ffmpeg path:', shutil.which('ffmpeg'))
for m in ['flask','groq','croniter','googleapiclient','google.oauth2','imageio_ffmpeg','moviepy','PIL']:
 try:
 importlib.import_module(m)
 print('OK', m)
 except Exception as e:
 print('MISSING', m)

print('token_new_channel.json exists:', os.path.exists('memory/token_new_channel.json'))
print('token.pickle exists:', os.path.exists('config/token.pickle'))
print('channels.json exists:', os.path.exists('config/channels.json'))
print('GROQ key set:', bool(os.environ.get('GROQ_API_KEY')))

if not os.environ.get('GROQ_API_KEY') and os.path.exists('.env'):
 for line in open('.env', encoding='utf-8'):
 if line.startswith('GROQ_API_KEY='):
 os.environ['GROQ_API_KEY'] = line.split('=',1)[1].strip()
 print('loaded GROQ key from .env:', bool(os.environ['GROQ_API_KEY']))
