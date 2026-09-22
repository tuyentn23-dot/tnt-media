import json, io
led=json.load(io.open('channels/Mialinhcute/published_ledger.json',encoding='utf-8'))
sigs=led.get('signatures',{})
for s,m in sigs.items():
    if 'meme' in s:
        print('meme sig:', s[:60], '->', m.get('youtube_id'))
