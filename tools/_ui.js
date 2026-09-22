
const TABS=[['dashboard','Dashboard','DASH','Tong quan he thong'],['channels','Kenh','CH','Quan ly kenh'],['multich','Da kenh','MC','Auto dang nhieu kenh'],['agent','Agent','BOT','Mo web - chup man hinh - lenh'],['videos','Video','VID','Thu vien video'],['plan','Plan','PLAN','Doc insight & lap ke hoach'],['do','Do','DO','Thuc thi cong cu'],['check','Check','CHECK','Do luong & phan tich'],['act','Act','ACT','Quyet dinh toi uu'],['tools','Cong cu','TOOLS','Registry 118 tool'],['scheduler','Scheduler','SCHED','Tu dong chay PDCA'],['studio','Studio','STUD','Build video chat luong cao'],['exp','A/B Test','EXP','Thi nghiem toi uu'],['settings','Settings','SET','Cau hinh he thong']];
let cur='dashboard';
function toast(m,t){const x=document.getElementById('toast');x.textContent=m;x.className='toast show '+(t||'');clearTimeout(x._t);x._t=setTimeout(()=>x.className='toast',3500)}
async function api(p,o){const r=await fetch('/os/api/'+p,o||{});return r.json()}
function fmt(n){return n==null||n===''?'-':Number(n).toLocaleString('vi-VN')}
function esc(s){return String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&','<':'<','>':'>'}[c]))}
function scoreBadge(s){if(s==null)return '<span class="badge b-mut">chua cham</span>';const c=s>=75?'b-ok':s>=50?'b-warn':'b-bad';return '<span class="badge '+c+'">'+s+'</span>'}
function statusBadge(s){const m={published:'b-ok',created:'b-mut',blocked:'b-bad',draft:'b-warn'};return '<span class="badge '+(m[s]||'b-mut')+'">'+esc(s)+'</span>'}
function buildNav(){const n=document.getElementById('nav');n.innerHTML='';TABS.forEach(t=>{const b=document.createElement('button');if(t[0]===cur)b.className='on';b.onclick=()=>go(t[0]);b.innerHTML='<span class="ic">'+t[2]+'</span> '+t[1];n.appendChild(b)})}
function go(t){cur=t;buildNav();const x=TABS.find(a=>a[0]===t);document.getElementById('title').textContent=x[1];document.getElementById('subtitle').textContent=x[3];render()}
async function render(){const c=document.getElementById('content');c.innerHTML='<div class="empty"><span class="spin"></span> Dang tai...</div>';const f={dashboard:dash,agent:agent,videos:videos,multich:multich,channels:channels,plan:plan,do:doTab,check:check,act:act,tools:tools,scheduler:sched,studio:studio,exp:expTab,settings:settings}[cur];try{await f()}catch(e){c.innerHTML='<div class="empty">Loi: '+esc(e.message)+'</div>'}}


async function dash(){
 const c=document.getElementById('content');
 const [v,i,d,cy]=await Promise.all([api('videos'),api('insights?limit=10'),api('decisions?limit=10'),api('cycles?limit=10')]);
 const vids=v.items||[],ins=i.items||[],dec=d.items||[],cys=cy.items||[];
 const pub=vids.filter(x=>x.status==='published').length;
 const scored=vids.filter(x=>x.score!=null);
 const avg=scored.length?Math.round(scored.reduce((a,b)=>a+b.score,0)/scored.length):null;
 let h='<div class="cards">';
 h+='<div class="card"><div class="lbl">Video tong</div><div class="val grad">'+fmt(vids.length)+'</div><div class="hint">'+pub+' da publish</div></div>';
 h+='<div class="card"><div class="lbl">Diem CL TB</div><div class="val">'+(avg==null?'-':avg)+'</div><div class="hint">'+(scored.length?scored.length+' da cham':'chua co')+'</div></div>';
 h+='<div class="card"><div class="lbl">Insights</div><div class="val">'+fmt(ins.length)+'</div></div>';
 h+='<div class="card"><div class="lbl">Quyet dinh</div><div class="val">'+fmt(dec.length)+'</div></div>';
 h+='</div>';
 h+='<div class="panel"><h2>Video gan day</h2>'+videoTable(vids.slice(0,8))+'</div>';
 h+='<div class="panel"><h2>Insight moi nhat</h2>'+listBlock(ins,'finding')+'</div>';
 h+='<div class="chartbox"><h2>Diem chat luong video</h2><canvas id="chartScore" height="240"></canvas></div>';
 c.innerHTML=h;
 setTimeout(function(){var vs=vids.filter(function(x){return x.score!=null});drawBars('chartScore',vs.map(function(x){return Math.round(x.score)}),vs.map(function(x){return '#'+x.id}));},60);
}
function videoTable(items){
 if(!items.length)return '<div class="empty">Chua co video</div>';
 let h='<table><thead><tr><th>ID</th><th>Tieu de</th><th>Topic</th><th>Score</th><th>Trang thai</th><th>YouTube</th></tr></thead><tbody>';
 items.forEach(v=>{h+='<tr><td>'+v.id+'</td><td>'+esc(v.title||'-')+'</td><td>'+esc(v.topic||'-')+'</td><td>'+scoreBadge(v.score)+'</td><td>'+statusBadge(v.status)+'</td><td>'+(v.youtube_id?'<a style="color:var(--acc)" target="_blank" href="https://youtu.be/"+v.youtube_id+">"+v.youtube_id+"</a>':'-')+'</td></tr>'});
 return h+'</tbody></table>';
}
function listBlock(items,key){
 if(!items.length)return '<div class="empty">Chua co du lieu</div>';
 return '<div>'+items.map(x=>'<div style="padding:8px 0;border-bottom:1px solid var(--line)">'+esc(x[key]||x.finding||x.kind||'')+'</div>').join('')+'</div>';
}
async function plan(){const c=document.getElementById('content');const i=await api('insights?limit=20');const ins=i.items||[];
 let h='<div class="panel"><h2>Insight dau vao (PLAN doc)</h2>'+listBlock(ins,'finding')+'</div>';
 h+='<div class="panel"><h2>Chay chu ky PDCA</h2><div class="row"><input id="goal" placeholder="Muc tieu (tuy chon)" style="flex:1;min-width:220px"><button class="btn ok" onclick="runCycle()">Bat dau PLAN</button></div><div class="muted">PLAN doc insight -> DO goi tool -> CHECK do luong -> ACT quyet dinh</div></div>';
 c.innerHTML=h;
}
async function doTab(){const c=document.getElementById('content');const t=await api('tools');const list=(t.tools||[]);
 let h='<div class="panel"><h2>Chay mot tool (DO)</h2><div class="row"><select id="tool" style="flex:1;min-width:220px">'+list.map(x=>'<option value="'+esc(x.file)+'">'+esc(x.file)+' ['+esc(x.cat)+']</option>').join('')+'</select><button class="btn" onclick="runTool()">Chay</button></div><pre id="toolout" style="display:none"></pre></div>';
 h+='<div class="panel"><h2>Tool registry ('+list.length+')</h2>'+toolsTable(list.slice(0,40))+'</div>';
 c.innerHTML=h;
}
function toolsTable(list){if(!list.length)return '<div class="empty">Khong co tool</div>';let h='<table><thead><tr><th>File</th><th>Nhom</th><th>Mo ta</th></tr></thead><tbody>';list.forEach(x=>{h+='<tr><td>'+esc(x.file)+'</td><td><span class="badge b-mut">'+esc(x.cat)+'</span></td><td class="muted">'+esc(x.doc||'')+'</td></tr>'});return h+'</tbody></table>';}
async function runTool(){const f=document.getElementById('tool').value;const o=document.getElementById('toolout');o.style.display='block';o.textContent='Dang chay...';try{const r=await api('do/run?tool='+encodeURIComponent(f),{method:'POST'});o.textContent=JSON.stringify(r,null,2);toast('Da chay '+f,'ok')}catch(e){o.textContent='Loi: '+e.message;toast('Loi','bad')}}


async function check(){const c=document.getElementById('content');const m=await api('metrics?limit=50');const ms=m.items||[];
 let h='<div class="panel"><h2>Do luong (CHECK)</h2><div class="row"><button class="btn" onclick="ingest()">Ingest metrics YouTube</button><span class="muted">Lay views/likes + quality audit</span></div><pre id="ingout" style="display:none"></pre></div>';
 h+='<div class="panel"><h2>Metrics gan day ('+ms.length+')</h2>'+metricsTable(ms.slice(0,30))+'</div>';
 c.innerHTML=h;
}
function metricsTable(items){if(!items.length)return '<div class="empty">Chua co metrics</div>';let h='<table><thead><tr><th>Video ID</th><th>Views</th><th>Likes</th><th>Comments</th><th>Nguon</th></tr></thead><tbody>';items.forEach(x=>{h+='<tr><td>'+esc(x.video_id)+'</td><td>'+fmt(x.views)+'</td><td>'+fmt(x.likes)+'</td><td>'+fmt(x.comments)+'</td><td class="muted">'+esc(x.source||'')+'</td></tr>'});return h+'</tbody></table>';}
async function ingest(){const o=document.getElementById('ingout');o.style.display='block';o.textContent='Dang ingest...';try{const r=await api('check/ingest?limit=10',{method:'POST'});o.textContent=JSON.stringify(r,null,2);toast('Ingest xong','ok');check()}catch(e){o.textContent='Loi: '+e.message;toast('Loi','bad')}}
async function act(){const c=document.getElementById('content');const d=await api('decisions?limit=50');const ds=d.items||[];
 let h='<div class="panel"><h2>Quyet dinh (ACT)</h2>';
 if(!ds.length)h+='<div class="empty">Chua co quyet dinh. Chay PDCA de sinh.</div>';
 else{h+='<table><thead><tr><th>Kind</th><th>Hanh dong</th></tr></thead><tbody>';ds.forEach(x=>{h+='<tr><td><span class="badge b-mut">'+esc(x.kind||'')+'</span></td><td><pre style="margin:0;max-height:120px">'+esc(JSON.stringify(x.evidence||x,null,1))+'</pre></td></tr>'});h+='</tbody></table>'}
 h+='</div>';
 c.innerHTML=h;
}
async function tools(){const c=document.getElementById('content');const t=await api('tools');const list=(t.tools||[]);const cats=t.by_cat||{};
 let h='<div class="cards"><div class="card"><div class="lbl">Tong tool</div><div class="val grad">'+fmt(t.total||list.length)+'</div></div>';
 Object.keys(cats).forEach(k=>{h+='<div class="card"><div class="lbl">'+esc(k)+'</div><div class="val">'+cats[k]+'</div></div>'});
 h+='</div><div class="panel"><h2>Danh sach tool</h2>'+toolsTable(list)+'</div>';
 c.innerHTML=h;
}
async function sched(){const c=document.getElementById('content');const s=await api('scheduler');
 let h='<div class="panel"><h2>Trang thai Scheduler</h2><div class="row"><span class="badge '+(s.running?'b-ok':'b-mut')+'">'+(s.running?'DANG CHAY':'DUNG')+'</span><span class="muted">interval: '+fmt(s.interval_sec)+'s</span></div>';
 h+='<div class="row"><button class="btn ok" onclick="schedStart()">Bat dau</button><button class="btn bad" onclick="schedStop()">Dung</button><button class="btn ghost" onclick="sched()">Lam moi</button></div>';
 h+='<pre>'+esc(JSON.stringify(s,null,2))+'</pre></div>';
 c.innerHTML=h;
}
async function schedStart(){try{await api('scheduler/start?interval_sec=3600',{method:'POST'});toast('Scheduler da bat','ok');sched()}catch(e){toast('Loi: '+e.message,'bad')}}
async function schedStop(){try{await api('scheduler/stop',{method:'POST'});toast('Scheduler da dung','ok');sched()}catch(e){toast('Loi: '+e.message,'bad')}}
function drawBars(canvasId, values, labels, color){
const cv=document.getElementById(canvasId); if(!cv) return;
const ctx=cv.getContext("2d"); const W=cv.width=cv.clientWidth2; const H=cv.height=260;
ctx.scale(1,1); ctx.clearRect(0,0,W,H);
const n=values.length; if(!n){ctx.fillStyle="#8b97a8";ctx.font="24px sans-serif";ctx.fillText("Chua co du lieu",20,40);return}
const max=Math.max.apply(null,values)||1; const pad=40; const bw=(W-pad*2)/n*0.6; const gap=(W-pad*2)/n;
for(let i=0;i<n;i++){const h=(values[i]/max)(H-80); const x=pad+igap+gap*0.2; const y=H-40-h;
const g=ctx.createLinearGradient(0,y,0,H-40); g.addColorStop(0,color||"#4f8cff"); g.addColorStop(1,"#9b5cff"); ctx.fillStyle=g; ctx.fillRect(x,y,bw,h);
ctx.fillStyle="#e6edf3"; ctx.font="bold 22px sans-serif"; ctx.textAlign="center"; ctx.fillText(values[i],x+bw/2,y-8);
ctx.fillStyle="#8b97a8"; ctx.font="18px sans-serif"; ctx.fillText((labels[i]||"").slice(0,6),x+bw/2,H-12);}}
async function studio(){
const c=document.getElementById('content');
let h='<div class="panel"><h2>Studio - Build video chat luong cao</h2>';
h+='<div class="row"><input id="stHook" placeholder="Hook text" style="flex:1;min-width:200px"><input id="stDur" value="12" style="width:80px"><button class="btn ok" onclick="stBuild()">Build</button><button class="btn" onclick="stAuto()" style="background:#2ecc71">Auto Publish</button></div>';
h+='<pre id="stOut">San sang...</pre></div>';
h+='<div class="panel"><h2>Xep hang footage</h2><div class="row"><button class="btn ghost" onclick="stRank()">Tai ranking</button></div><pre id="stRank">Bam de tai...</pre></div>';
c.innerHTML=h}
async function stRank(){const o=document.getElementById("stRank");o.textContent="Dang phan tich...";try{const d=await api("quality/ranking?limit=12");o.textContent=JSON.stringify(d,null,2)}catch(e){o.textContent="Loi: "+e.message}}
async function stBuild(){const o=document.getElementById("stOut");o.textContent="Dang build (1-3 phut)...";const hook=document.getElementById("stHook").value;const dur=document.getElementById("stDur").value;try{const r=await fetch("/os/api/build?paths=%5B%5D&hook="+encodeURIComponent(hook)+"&target_dur="+dur,{method:"POST"});const d=await r.json();o.textContent=JSON.stringify(d,null,2);toast("Build xong","ok")}catch(e){o.textContent="Loi: "+e.message}}
async function expTab(){
const c=document.getElementById('content');const d=await api('experiments');const ex=d.items||[];
let h='<div class="panel"><h2>Tao thi nghiem A/B</h2><div class="row"><input id="expName" placeholder="Ten thi nghiem" style="flex:1;min-width:180px"><input id="expA" placeholder="Variant A" style="width:140px"><input id="expB" placeholder="Variant B" style="width:140px"><button class="btn ok" onclick="expCreate()">Tao</button></div></div>';
h+='<div class="panel"><h2>Danh sach thi nghiem ('+ex.length+')</h2>';
if(!ex.length)h+='<div class="empty">Chua co thi nghiem</div>';
else{h+='<table><thead><tr><th>ID</th><th>Ten</th><th>A</th><th>B</th><th>Metric</th><th>Winner</th><th></th></tr></thead><tbody>';
ex.forEach(function(x){h+='<tr><td>'+x.id+'</td><td>'+esc(x.name)+'</td><td>'+esc(x.variant_a)+'</td><td>'+esc(x.variant_b)+'</td><td>'+esc(x.metric)+'</td><td>'+(x.winner?'<span class="badge b-ok">'+x.winner+'</span>':'-')+'</td><td>'+(x.winner?'':'<button class="btn" onclick="expWin('+x.id+','+x.variant_a+')">A thang</button> <button class="btn" onclick="expWin('+x.id+','+x.variant_b+')">B thang</button>')+'</td></tr>'});h+='</tbody></table>';}
h+='</div>';c.innerHTML=h}
async function expCreate(){const n=document.getElementById('expName').value;const a=document.getElementById('expA').value;const b=document.getElementById('expB').value;try{await fetch('/os/api/experiments?name='+encodeURIComponent(n)+'&variant_a='+encodeURIComponent(a)+'&variant_b='+encodeURIComponent(b),{method:'POST'});toast('Da tao','ok');expTab()}catch(e){toast('Loi: '+e.message,'bad')}}
async function expWin(eid,w){try{await fetch('/os/api/experiments/decide?eid='+eid+'&winner='+encodeURIComponent(w),{method:'POST'});toast('Da chon: '+w,'ok');expTab()}catch(e){toast('Loi','bad')}}
async function stAuto(){
const o=document.getElementById("stOut");
o.textContent="Auto: build + publish...";
const dur=document.getElementById("stDur").value;
try{const r=await fetch("/os/api/autopublish?target_dur="+dur,{method:"POST"});
const d=await r.json();o.textContent=JSON.stringify(d,null,2);
toast(d.ok?"Da dang!":"Blocked",d.ok?"ok":"bad")}
catch(e){o.textContent="Loi: "+e.message}}
async function agent(){const c=document.getElementById("content");
let h="<div class=panel><h2>Cong cu Agent</h2>";
h+="<div class=row><input id=agUrl value=https:// style=flex:1;min-width:240px><button class=btn ok onclick=agOpen()>Mo web</button>";
h+="<button class=btn onclick=agShot()>Chup man hinh</button><button class=btn onclick=agScreen()>Doc chu man hinh</button></div>";
h+="<div class=row><input id=agCmd placeholder='lenh...' style=flex:1;min-width:240px><button class=btn onclick=agRun()>Chay lenh</button></div>";
h+="<pre id=agOut style=white-space:pre-wrap;font-size:12px;max-height:300px;overflow:auto></pre>";
h+="<h3>Nhat ky hanh dong</h3><div id=agLog style=max-height:300px;overflow:auto></div></div>";
c.innerHTML=h;agLog();}
async function agOpen(){const u=document.getElementById("agUrl").value;const r=await fetch("/os/api/agent/open_url?url="+encodeURIComponent(u),{method:"POST"});document.getElementById("agOut").textContent=JSON.stringify(await r.json(),null,2)}
async function agShot(){const r=await fetch("/os/api/agent/screenshot",{method:"POST"});document.getElementById("agOut").textContent=JSON.stringify(await r.json(),null,2)}
async function agScreen(){const r=await fetch("/os/api/agent/read_screen",{method:"POST"});document.getElementById("agOut").textContent=JSON.stringify(await r.json(),null,2)}
async function agRun(){const cmd=document.getElementById("agCmd").value;const r=await fetch("/os/api/agent/run_cmd?cmd="+encodeURIComponent(cmd),{method:"POST"});document.getElementById("agOut").textContent=JSON.stringify(await r.json(),null,2)}
async function agLog(){const r=await fetch("/os/api/agent/actions?limit=30");const d=await r.json();let h="<table><thead><tr><th>Thoi gian</th><th>Hanh dong</th><th>Chi tiet</th></tr></thead><tbody>";(d.items||[]).forEach(x=>{h+="<tr><td>"+x.ts+"</td><td>"+x.action+"</td><td>"+String(x.detail).slice(0,80)+"</td></tr>"});h+="</tbody></table>";document.getElementById("agLog").innerHTML=h}
async function videos(){const c=document.getElementById('content');let h='<div class=panel><h2>Thu vien Video</h2>';h+= '<div class=row><input id=vidFilter placeholder=Loc-ten oninput=vidRender() style=flex:1;min-width:200px><button class=btn onclick=videos()>Lam moi</button></div><div id=vidGrid class=grid></div></div>';c.innerHTML=h;try{const r=await fetch('/os/api/gallery?limit=80');const d=await r.json();window._vids=d.items||[];vidRender();}catch(e){c.innerHTML+= '<p>Loi: '+e.message+'</p>';}}
function vidRender(){const g=document.getElementById('vidGrid');if(!g)return;const q=(document.getElementById('vidFilter')||{}).value||'';const list=(window._vids||[]).filter(v=>!q||v.name.toLowerCase().includes(q.toLowerCase()));let h='';list.forEach(function(v){const mb=(v.size/1048576).toFixed(1);const dt=new Date(v.mtime*1000).toLocaleString();h+='<div class=vcard><video src='+v.url+' preload=metadata muted></video><div class=vmeta><div class=vname>'+v.name+'</div><div class=vsub>'+mb+' MB - '+dt+'</div></div></div>';});g.innerHTML=h||'<p>Khong co video</p>';}

async function multich(){const c=document.getElementById('content');
let h='<div class=panel><h2>Auto dang nhieu kenh</h2>';h+='<div class=row><button class="btn ok" onclick="mcRun()">Chay auto dang</button> ';h+='<button class="btn" onclick="mcState()">Trang thai</button></div>';h+='<pre id="mcOut" style="white-space:pre-wrap;font-size:12px"></pre></div>';c.innerHTML=h;mcState();}
async function mcRun(){const o=document.getElementById('mcOut');o.textContent='Dang chay...';try{const r=await fetch('/os/api/multichannel/run',{method:'POST'});const d=await r.json();o.textContent=JSON.stringify(d,null,2)}catch(e){o.textContent='Loi: '+e.message}}
async function mcState(){const o=document.getElementById('mcOut');try{const r=await fetch('/os/api/multichannel/state');const d=await r.json();o.textContent=JSON.stringify(d,null,2)}catch(e){o.textContent='Loi: '+e.message}}
async function channels(){const c=document.getElementById('content');try{const r=await fetch('/os/api/channels');const d=await r.json();let h='<div class=panel><h2>Quan ly kenh</h2><table><tbody>';(d.items||[]).forEach(function(x){h+='<tr><td>'+x.id+'</td><td>'+(x.name||'')+'</td><td>'+(x.enabled?'ON':'OFF')+'</td></tr>';});h+='</tbody></table></div>';c.innerHTML=h;}catch(e){c.innerHTML='Loi: '+e.message}}
async function chToggle(id,en){await fetch('/os/api/channels/'+id+'/toggle?enabled='+en,{method:'POST'});channels();}


async function settings(){const c=document.getElementById('content');const s=await api('settings');
 let h='<div class="panel"><h2>Cau hinh</h2><table><tbody>';
 Object.keys(s).forEach(k=>{const ok=s[k];h+='<tr><td>'+esc(k)+'</td><td><span class="badge '+(ok?'b-ok':'b-bad')+'">'+(ok?'OK':'THIEU')+'</span></td></tr>'});
 h+='</tbody></table></div>';
 c.innerHTML=h;
}
async function runCycle(){const b=document.getElementById('btnCycle');b.disabled=true;const old=b.textContent;b.textContent='Dang chay...';try{const r=await api('run_cycle',{method:'POST'});toast('PDCA xong','ok');go(cur)}catch(e){toast('Loi: '+e.message,'bad')}b.disabled=false;b.textContent=old}
buildNav();render();
