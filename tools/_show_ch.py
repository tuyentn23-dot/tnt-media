js=open('tools/_ui.js',encoding='utf-8').read()
i=js.find('async function channels()')
print(js[i:i+1200].encode('ascii','replace').decode('ascii'))
