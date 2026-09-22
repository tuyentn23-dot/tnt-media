P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
start=s.find('async function channels()')
nxt=s.find(chr(10)+'async function ', start+10)
print('replace', start, nxt)
Q=chr(39)
new=(
"async function channels(){const c=document.getElementById("+Q+"content"+Q+");"
"try{const r=await fetch("+Q+"/os/api/channels"+Q+");const d=await r.json();"
"let h="+Q+"<div class=panel><h2>Quan ly kenh</h2><table><thead><tr><th>ID</th><th>Ten</th><th>Bat</th><th>Kinds</th><th>Video moi</th><th>Da dang</th><th></th></tr></thead><tbody>"+Q+";"
"(d.items||[]).forEach(function(x){h+="+Q+"<tr><td>"+Q+"+x.id+"+Q+"</td><td>"+Q+"+(x.name||"+Q+""+Q+")+"+Q+"</td>"+Q+";"
"h+="+Q+"<td><span class=badge>"+Q+"+(x.enabled?"+Q+"ON"+Q+":"+Q+"OFF"+Q+")+"+Q+"</span></td>"+Q+";"
"h+="+Q+"<td>"+Q+"+((x.kinds||[]).join("+Q+", "+Q+"))+"+Q+"</td>"+Q+";"
"h+="+Q+"<td>"+Q+"+JSON.stringify(x.fresh||{})+"+Q+"</td>"+Q+";"
"h+="+Q+"<td>"+Q+"+(x.published||0)+"+Q+"</td>"+Q+";"
"h+="+Q+"<td><button class=btn onclick=chToggle("+Q+""+Q+"+x.id+"+Q+""+Q+","+Q+""+Q+"+(x.enabled?"+Q+"false"+Q+":"+Q+"true"+Q+")+"+Q+""+Q+")>"+Q+"+(x.enabled?"+Q+"Tat"+Q+":"+Q+"Bat"+Q+")+"+Q+"</button></td></tr>"+Q+";});"
"h+="+Q+"</tbody></table></div>"+Q+";c.innerHTML=h;}catch(e){c.innerHTML="+Q+"Loi: "+Q+"+e.message}}\n"
"async function chToggle(id,en){await fetch("+Q+"/os/api/channels/"+Q+"+id+"+Q+"/toggle?enabled="+Q+"+en,{method:"+Q+"POST"+Q+"});toast("+Q+"Da cap nhat "+Q+"+id,"+Q+"ok"+Q+");channels();}\n"
)
s2=s[:start]+new+s[nxt:]
open(P,'w',encoding='utf-8').write(s2)
i=s2.find('<script>'); j=s2.rfind('</script>')
open('tools/_ui.js','w',encoding='utf-8').write(s2[i+8:j])
print('rewritten channels')
