P = 'os_app/ui/index.html'
s = open(P, encoding='utf-8', errors='replace').read()

# 1) add tab entry before closing of TABS array: insert after ['dashboard',...]
old_tab = "['dashboard','Dashboard','DASH','Tong quan he thong'],"
new_tab = old_tab + "['channels','Kenh','CH','Quan ly kenh'],"
if 'channels' not in s[:6000]:
    s = s.replace(old_tab, new_tab, 1)
    print('tab added')
else:
    print('tab exists')

# 2) add channels() JS function before async function settings()
marker = 'async function settings()'
fn = (
 "async function channels(){const c=document.getElementById('content');"
 "try{const r=await fetch('/os/api/channels');const d=await r.json();"
 "let h='<div class=panel><h2>Quan ly kenh</h2><table><thead><tr><th>ID</th><th>Ten</th><th>Bat</th><th>Kinds</th><th>Video moi</th><th>Da dang</th><th></th></tr></thead><tbody>';"
 "(d.items||[]).forEach(function(x){h+='<tr><td>'+x.id+'</td><td>'+(x.name||'')+'</td>';"
 "h+='<td><span class=\"badge '+(x.enabled?'b-ok':'b-bad')+'\">'+(x.enabled?'ON':'OFF')+'</span></td>';"
 "h+='<td>'+((x.kinds||[]).join(', '))+'</td>';"
 "h+='<td>'+JSON.stringify(x.fresh||{})+'</td>';"
 "h+='<td>'+(x.published||0)+'</td>';"
 "h+='<td><button class=btn onclick=\"chToggle(\''+x.id+'\','+(x.enabled?'false':'true')+')\">'+(x.enabled?'Tat':'Bat')+'</button></td></tr>'});"
 "h+='</tbody></table></div>';c.innerHTML=h;}catch(e){c.innerHTML='Loi: '+e.message}}"
 "async function chToggle(id,en){await fetch('/os/api/channels/'+id+'/toggle?enabled='+en,{method:'POST'});toast('Da cap nhat '+id,'ok');channels();}"
)
if 'async function channels()' not in s:
    s = s.replace(marker, fn + chr(10) + marker, 1)
    print('fn added')
else:
    print('fn exists')

# 3) register renderer: find where render() dispatches functions (e.g. if(name==='tools') tools();)
open(P, 'w', encoding='utf-8').write(s)
print('written len', len(s))
