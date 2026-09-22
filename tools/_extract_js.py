s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
i=s.find('<script>')
j=s.rfind('</script>')
js=s[i+8:j]
open('tools/_ui.js','w',encoding='utf-8').write(js)
print('extracted js len', len(js))
