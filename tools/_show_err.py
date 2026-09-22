js=open('tools/_ui.js',encoding='utf-8').read().splitlines()
for i in range(141,145):
    if i<len(js):
        print(i+1, js[i].encode('ascii','replace').decode('ascii'))
