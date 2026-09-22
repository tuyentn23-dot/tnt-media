import json
d = json.load(open('youtube_growth_strategy.json', encoding='utf-8'))
def flat(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            flat(v, p + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            flat(v, p + '[%rs]' % i)
    else:
        s = str(o).encode('ascii', 'replace').decode()
        print(p, '=', s)
flat(d)
