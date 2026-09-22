s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
js=s[s.find('<script'):s.rfind('</script>')]
# In 1500 ky tu cuoi JS (phan init)
print(js[-1500:].encode('ascii','replace').decode('ascii'))
