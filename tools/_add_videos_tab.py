import io, base64
P='os_app/ui/index.html'
s=io.open(P,encoding='utf-8',errors='replace').read()
js=base64.b64decode(open('tools/_videos_js.b64').read().strip()).decode('utf-8')
# 1) add tab
old="['multich','Da kenh','MC','Auto dang nhieu kenh'],"
new=old+"['videos','Video','VID','Thu vien video'],"
if 'videos' not in s[:6500]:
    s=s.replace(old,new,1); print('tab added')
# 2) add function before multich
marker='async function multich()'
if 'async function videos()' not in s:
    s=s.replace(marker, js+chr(10)+marker, 1); print('fn added')
# 3) register renderer
oldm='{dashboard:dash,multich:multich,'
newm='{dashboard:dash,videos:videos,multich:multich,'
if oldm in s:
    s=s.replace(oldm,newm,1); print('renderer registered')
# 4) add CSS for grid
css='.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}.vcard{background:var(--panel2);border:1px solid var(--line);border-radius:8px;overflow:hidden}.vcard video{width:100%;height:140px;object-fit:cover;background:#000}.vmeta{padding:8px}.vname{font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--txt)}.vsub{font-size:11px;color:var(--mut);margin-top:3px}'
if '.vcard' not in s:
    s=s.replace('</style>', css+'</style>',1); print('css added')
io.open(P,'w',encoding='utf-8').write(s)
print('written', len(s))
