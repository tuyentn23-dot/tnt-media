import io, json
p = 'channels/whatif_vi/channel.json'
cfg = json.load(io.open(p, encoding='utf-8'))
cfg['name'] = 'What If Viet'
cfg['enabled'] = True
cfg['token_file'] = 'token.pickle'
cfg['content']['kinds'] = ['whatif', 'facts']
cfg['content']['category_id'] = '28'
cfg['content']['tags_base'] = ['shorts', 'whatif', 'kham pha']
cfg['style']['watermark'] = '@whatifvi'
io.open(p, 'w', encoding='utf-8').write(json.dumps(cfg, ensure_ascii=False, indent=2))
print('UPDATED')
print(json.dumps(cfg, ensure_ascii=False, indent=2))
