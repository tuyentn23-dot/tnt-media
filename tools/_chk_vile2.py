import json, io, os, time
led='channels/vilevi5676/published_ledger.json'
d=json.load(io.open(led,encoding='utf-8'))
print('vile published:', len(d.get('signatures',{})))
for s,m in d.get('signatures',{}).items():
    print(' ', s.split('|')[1], '->', m.get('youtube_id'))
files=sorted([f for f in os.listdir('output') if f.startswith('chvilevi5676')], key=lambda f: os.path.getmtime('output/'+f), reverse=True)
for f in files[:6]:
    print(time.strftime('%H:%M:%S', time.localtime(os.path.getmtime('output/'+f))), f, os.path.getsize('output/'+f))
