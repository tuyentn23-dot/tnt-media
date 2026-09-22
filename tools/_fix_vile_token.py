import json, io
P='channels/vilevi5676/channel.json'
d=json.load(io.open(P,encoding='utf-8'))
d['token_file']='config/token.pickle'
json.dump(d, io.open(P,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('token_file ->', d['token_file'])
from ops import channel_loader as ch
cfg=ch.load('vilevi5676')
print('resolved:', ch.token_path(cfg))
import os
print('exists:', os.path.exists(ch.token_path(cfg)))
