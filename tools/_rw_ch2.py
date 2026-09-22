P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
start=s.find('async function channels()')
nxt=s.find(chr(10)+'async function ', start+10)
DQ=chr(34)
# JS string in double quotes, HTML attrs unquoted, avoid single quotes inside except JS 'content'
new=(
'async function channels(){const c=document.getElementById('+DQ+'content'+DQ+');'
'try{const r=await fetch('+DQ+'/os/api/channels'+DQ+');const d=await r.json();'
'let h='+DQ+'<div class=panel><h2>Quan ly kenh</h2><table><thead><tr><th>ID</th><th>Ten</th><th>Bat</th><th>Kinds</th><th>Video moi</th><th>Da dang</th><th></th></tr></thead><tbody>'+DQ+';'
'(d.items||[]).forEach(function(x){'
'h+='+DQ+'<tr><td>'+DQ+'+x.id+'+DQ+'</td><td>'+DQ+'+(x.name||'+DQ+DQ+')+'+DQ+'</td>'+DQ+';'
'h+='+DQ+'<td>'+(x.enabled?'+DQ+'ON'+DQ+':'+DQ+'OFF'+DQ+')+'+DQ+'</td>'+DQ+';'
'h+='+DQ+'<td>'+DQ+'+((x.kinds||[]).join('+DQ+', '+DQ+'))+'+DQ+'</td>'+DQ+';'
'h+='+DQ+'<td>'+DQ+'+JSON.stringify(x.fresh||{})+'+DQ+'</td>'+DQ+';'
'h+='+DQ+'<td>'+DQ+'+(x.published||0)+'+DQ+'</td>'+DQ+';'
'h+='+DQ+'<td><button class=btn onclick=chToggle('+DQ+'+x.id+'+DQ+','+DQ+'+(x.enabled?'+DQ+'false'+DQ+':'+DQ+'true'+DQ+')+'+DQ+')>'+DQ+'+(x.enabled?'+DQ+'Tat'+DQ+':'+DQ+'Bat'+DQ+')+'+DQ+'</button></td></tr>'+DQ+';});'
'h+='+DQ+'</tbody></table></div>'+DQ+';c.innerHTML=h;}catch(e){c.innerHTML='+DQ+'Loi: '+DQ+'+e.message}}'+chr(10)
'async function chToggle(id,en){await fetch('+DQ+'/os/api/channels/'+DQ+'+id+'+DQ+'/toggle?enabled='+DQ+'+en,{method:'+DQ+'POST'+DQ+'});toast('+DQ+'Da cap nhat '+DQ+'+id,'+DQ+'ok'+DQ+');channels();}'+chr(10)
)
s2=s[:start]+new+s[nxt:]
open(P,'w',encoding='utf-8').write(s2)
i=s2.find('<script>'); j=s2.rfind('</script>')
open('tools/_ui.js','w',encoding='utf-8').write(s2[i+8:j])
print('rewritten ch2')
