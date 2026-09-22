P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
Q=chr(92)+chr(34)  # backslash-quote
bad='src='+Q+Q+'+v.url+'+Q+Q
print('bad repr:', repr(bad))
print('count:', s.count(bad))
s=s.replace(bad, 'src='+chr(34)+'+v.url+'+chr(34))
open(P,'w',encoding='utf-8').write(s)
# validate via node
i=s.find('<script>')
j=s.rfind('</script>')
open('tools/_ui.js','w',encoding='utf-8').write(s[i+8:j])
print('fixed + re-extracted')
