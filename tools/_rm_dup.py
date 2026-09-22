P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
# find all occurrences of 'async function chToggle'
idxs=[]
i=0
while True:
    i=s.find('async function chToggle', i)
    if i<0: break
    idxs.append(i); i+=1
print('occurrences:', idxs)
if len(idxs)>1:
    # remove the second one up to end-of-line
    start=idxs[1]
    end=s.find(chr(10), start)
    s=s[:start]+s[end+1:]
    open(P,'w',encoding='utf-8').write(s)
    print('removed dup')
    i=s.find('<script>'); j=s.rfind('</script>')
    open('tools/_ui.js','w',encoding='utf-8').write(s[i+8:j])
