P='os_app/ui/index.html'
s=open(P,encoding='utf-8',errors='replace').read()
start=s.find('async function videos()')
if start<0:
    print('videos fn not found'); raise SystemExit
# find end: next '\nasync function ' after start
nxt=s.find(chr(10)+'async function ', start+10)
if nxt<0: nxt=s.find('function vidRender', start)
end=nxt
print('replacing chars', start, 'to', end)
Q=chr(39)  # single quote for JS strings
new = (
"async function videos(){const c=document.getElementById("+Q+"content"+Q+");"
"let h="+Q+"<div class=panel><h2>Thu vien Video</h2>"+Q+";"
"h+= "+Q+"<div class=row><input id=vidFilter placeholder=Loc-ten oninput=vidRender() style=flex:1;min-width:200px><button class=btn onclick=videos()>Lam moi</button></div><div id=vidGrid class=grid></div></div>"+Q+";"
"c.innerHTML=h;"
"try{const r=await fetch("+Q+"/os/api/gallery?limit=80"+Q+");const d=await r.json();window._vids=d.items||[];vidRender();}catch(e){c.innerHTML+= "+Q+"<p>Loi: "+Q+"+e.message+"+Q+"</p>"+Q+";}}\n"
"function vidRender(){const g=document.getElementById("+Q+"vidGrid"+Q+");if(!g)return;"
"const q=(document.getElementById("+Q+"vidFilter"+Q+")||{}).value||"+Q+""+Q+";"
"const list=(window._vids||[]).filter(v=>!q||v.name.toLowerCase().includes(q.toLowerCase()));"
"let h="+Q+""+Q+";"
"list.forEach(function(v){const mb=(v.size/1048576).toFixed(1);const dt=new Date(v.mtime*1000).toLocaleString();"
"h+="+Q+"<div class=vcard><video src="+Q+"+v.url+"+Q+" preload=metadata muted></video><div class=vmeta><div class=vname>"+Q+"+v.name+"+Q+"</div><div class=vsub>"+Q+"+mb+"+Q+" MB - "+Q+"+dt+"+Q+"</div></div></div>"+Q+";});"
"g.innerHTML=h||"+Q+"<p>Khong co video</p>"+Q+";}\n"
)
s2 = s[:start] + new + s[end:]
open(P,'w',encoding='utf-8').write(s2)
# re-extract for node check
i=s2.find('<script>'); j=s2.rfind('</script>')
open('tools/_ui.js','w',encoding='utf-8').write(s2[i+8:j])
print('rewritten')
