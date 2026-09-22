s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
for name in ['async function agent()','async function videos()','async function multich()']:
    i=s.find(name)
    # tim ket thuc ham (dong trong)
    j=s.find('\n}\n', i)
    seg=s[i:j+2]
    print('===', name, 'len', len(seg), '===')
    print(seg.encode('ascii','replace').decode('ascii'))
    print()
