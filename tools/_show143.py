js=open('tools/_ui.js',encoding='utf-8').read().splitlines()
for i in range(140,146):
    if i < len(js):
        print(i+1, repr(js[i]))
