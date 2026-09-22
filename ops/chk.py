import json
d=json.load(open('config/scripts_vi.json',encoding='utf-8'))
out=[]
for k in ['animal','anime','roblox','cute_animals']:
    out.append(k + ': ' + json.dumps(d.get(k), ensure_ascii=True))
print(chr(10).join(out))
