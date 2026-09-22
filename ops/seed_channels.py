import os, json
ROOT = os.getcwd()
CH = os.path.join(ROOT, 'channels')
channels = [
 {'name': 'Mialinhcute', 'platform': 'youtube', 'active': True, 'aspect': '9:16', 'maxSeconds': 20, 'voicePreset': 'female_cute', 'voiceId': 'HoaiMy', 'colorPrimary': '#ff69b4', 'colorAccent': '#ffd700', 'watermark': '@Mialinhcute', 'topics': ['anime', 'roblox', 'cute_animals', 'meme', 'gacha'], 'audience': 'kids', 'romance': 'forbidden', 'tokenPath': 'memory/token_new_channel.json', 'scheduleCron': '0 9,15,21 * * *'},
 {'name': 'vilevi5676', 'platform': 'youtube', 'active': True, 'aspect': '9:16', 'maxSeconds': 90, 'voicePreset': 'female_warm', 'voiceId': 'calm', 'colorPrimary': '#2b6cb0', 'colorAccent': '#f6ad55', 'watermark': '@vilevi5676', 'topics': ['lifestyle', 'food', 'animals', 'nostalgia', 'curiosity', 'whatif', 'facts'], 'audience': 'general', 'romance': 'allowed', 'tokenPath': 'config/token.pickle', 'scheduleCron': '0 8,12,18,21 * * *'}
]
for c in channels:
 p = os.path.join(CH, c['name'] + '.json')
 f = open(p, 'w', encoding='utf-8')
 json.dump(c, f, ensure_ascii=False, indent=2)
 f.close()
 print('wrote', p, os.path.getsize(p), 'bytes')
print('done')
