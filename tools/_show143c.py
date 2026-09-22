js=open('tools/_ui.js',encoding='utf-8').read().splitlines()
line=js[142]
print('LEN', len(line))
# caret was near col 190-210, show 170-260
print(repr(line[170:280]))
