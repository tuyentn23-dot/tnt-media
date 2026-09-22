s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
js=s[s.find('<script'):s.rfind('</script>')]
print('LAST200:', js[-200:].encode('ascii','replace').decode('ascii'))
print()
print('GO:', s[s.find('function go('):s.find('function go(')+260].encode('ascii','replace').decode('ascii'))
