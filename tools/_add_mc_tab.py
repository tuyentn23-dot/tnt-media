# -*- coding: utf-8 -*-
import io
P = 'os_app/ui/index.html'
s = io.open(P, encoding='utf-8', errors='replace').read()
# 1) them tab multichannel
old_tab = "['channels','Kenh','CH','Quan ly kenh'],"
new_tab = old_tab + "['multich','Da kenh','MC','Auto dang nhieu kenh'],"
if 'multich' not in s[:6000]:
    s = s.replace(old_tab, new_tab, 1)
    print('tab added')
else:
    print('tab exists')
# 2) them ham multich() truoc async function settings
marker = 'async function channels()'
fn = (
 "async function multich(){const c=document.getElementById('content');"
 "let h='<div class=panel><h2>Auto dang nhieu kenh</h2>'"
 "+'<div class=row><button class=\"btn ok\" onclick=\"mcRun()\">Chay auto dang (2 video/kenh)</button> '"
 "+'<button class=\"btn\" onclick=\"mcState()\">Xem trang thai</button></div>'
 "+'<pre id=mcOut style=\"white-space:pre-wrap;font-size:12px\"></pre></div>';"
 "c.innerHTML=h;mcState();}"
 "async function mcRun(){const o=document.getElementById('mcOut');o.textContent='Dang chay...';"
 "try{const r=await fetch('/os/api/multichannel/run',{method:'POST'});const d=await r.json();o.textContent=JSON.stringify(d,null,2);toast('Xong','ok')}"
 "catch(e){o.textContent='Loi: '+e.message}}"
 "async function mcState(){const o=document.getElementById('mcOut');"
 "try{const r=await fetch('/os/api/multichannel/state');const d=await r.json();o.textContent=JSON.stringify(d,null,2)}"
 "catch(e){o.textContent='Loi: '+e.message}}"
)
if 'async function multich()' not in s:
    s = s.replace(marker, fn + chr(10) + marker, 1)
    print('fn added')
else:
    print('fn exists')
# 3) dang ky renderer
old_map = '{dashboard:dash,channels:channels,'
new_map = '{dashboard:dash,multich:multich,channels:channels,'
if old_map in s:
    s = s.replace(old_map, new_map, 1)
    print('renderer registered')
else:
    print('map not found')
io.open(P, 'w', encoding='utf-8').write(s)
print('written', len(s))
