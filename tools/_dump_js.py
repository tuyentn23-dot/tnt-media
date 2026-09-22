s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
# In toan bo phan JS tu <script> den </script>
i=s.find('<script>')
j=s.rfind('</script>')
js=s[i:j]
print('JS length:', len(js))
# Tim cac cho co the loi: TABS, render, go
k=js.find('const TABS=')
print('--- TABS ---')
print(js[k:k+400].encode('ascii','replace').decode('ascii'))
