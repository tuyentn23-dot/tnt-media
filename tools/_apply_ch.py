import base64
P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
fn=base64.b64decode(open('tools/_ch_fn.b64').read().strip()).decode('utf-8')
start=s.find('async function channels()')
nxt=s.find(chr(10)+'async function ', start+10)
print('replace', start, nxt)
s2=s[:start]+fn+s[nxt:]
open(P,'w',encoding='utf-8').write(s2)
i=s2.find('<script>'); j=s2.rfind('</script>')
open('tools/_ui.js','w',encoding='utf-8').write(s2[i+8:j])
print('applied')
