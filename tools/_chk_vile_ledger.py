import json, io
d=json.load(io.open('channels/vilevi5676/published_ledger.json',encoding='utf-8'))
print('vile published:', len(d.get('signatures',{})))
for sig,meta in d.get('signatures',{}).items():
    print(' ', meta.get('youtube_id'), '|', meta.get('kind'), '|', sig.split('|')[1])
