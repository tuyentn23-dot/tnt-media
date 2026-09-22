s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
js=s[s.find('<script'):s.rfind('</script>')]
# 1) TABS
k=js.find('const TABS=')
print('TABS:', js[k:k+320].encode('ascii','replace').decode('ascii'))
# 2) render dispatch
k=js.find('const f={')
print('DISPATCH:', js[k:k+260].encode('ascii','replace').decode('ascii'))
# 3) init / go
k=js.find('function go(')
print('GO:', js[k:k+200].encode('ascii','replace').decode('ascii'))
# 4) cuoi file init
print('TAIL:', js[-400:].encode('ascii','replace').decode('ascii'))
