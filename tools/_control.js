
const api=async(u,o)=>{const r=await fetch('/os/api/'+u,o||{});return r.json()};
const esc=s=>String(s==null?'':s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const toast=(m,k)=>{const t=document.getElementById('toast');t.textContent=m;t.style.display='block';t.style.borderColor=k==='ok'?'#2ecc71':k==='bad'?'#ff5c5c':'#1f2836';setTimeout(()=>t.style.display='none',2600)};
let cur='overview';
const TABS=[['overview','Tong quan'],['channels','Kenh'],['content','Noi dung'],['publish','Dang bai'],['history','Lich su'],['logs','Nhat ky']];
function tabs(){document.getElementById('tabs').innerHTML=TABS.map(t=>'<button class="'+(t[0]===cur?'on':'')+'" onclick="go(&quot;'+t[0]+'&quot;)">'+t[1]+'</button>').join('')}
function go(t){cur=t;tabs();render()}
async function stats(){
try{const d=await api('summary');const ch=await api('channels');
const items=ch.items||[];const pub=items.reduce((a,x)=>a+(x.published||0),0);const en=items.filter(x=>x.enabled).length;
document.getElementById('stats').innerHTML=
'<div class=card><div class=lbl>Kenh hoat dong</div><div class=val>'+en+'/'+items.length+'</div></div>'+
'<div class=card><div class=lbl>Tong video da dang</div><div class=val>'+pub+'</div></div>'+
'<div class=card><div class=lbl>Tong video</div><div class=val>'+(d.videos||0)+'</div></div>'+
'<div class=card><div class=lbl>Da publish</div><div class=val>'+(d.published||0)+'</div></div>';
}catch(e){document.getElementById('stats').innerHTML='<div class=card>Loi: '+esc(e.message)+'</div>'}}
async function render(){document.getElementById('view').innerHTML='<div class=panel>Dang tai...</div>';await stats();
if(cur==='overview')return ov();if(cur==='channels')return chs();if(cur==='content')return ct();if(cur==='publish')return pub();if(cur==='history')return hist();if(cur==='logs')return logs()}
async function ov(){const d=await api('summary');const c=await api('charts');
let h='<div class=panel><h2>Trang thai he thong</h2><pre>'+esc(JSON.stringify(d,null,2))+'</pre></div>';
h+='<div class=panel><h2>Bieu do theo chu de</h2><pre>'+esc(JSON.stringify(c,null,2))+'</pre></div>';
document.getElementById('view').innerHTML=h}
async function chs(){const d=await api('channels');const items=d.items||[];
let h='<div class=panel><h2>Quan ly kenh <button class="btn ok" onclick="runAll()">Auto dang tat ca (2/kenh)</button></h2><table><thead><tr><th>Kenh</th><th>Trang thai</th><th>Kinds</th><th>Video moi</th><th>Da dang</th><th>Hanh dong</th></tr></thead><tbody>';
items.forEach(x=>{const fresh=x.fresh||{};const total=Object.values(fresh).reduce((a,b)=>a+b,0);
h+='<tr><td><b>'+esc(x.name||x.id)+'</b><br><span style=color:#8b97a8;font-size:11px>'+esc(x.id)+'</span></td>';
h+='<td><span class="badge '+(x.enabled?'b-ok':'b-bad')+'">'+(x.enabled?'BAT':'TAT')+'</span></td>';
h+='<td>'+esc((x.kinds||[]).join(', '))+'</td>';
h+='<td>'+(total>0?'<span class="badge b-warn">'+total+' moi</span>':'0')+'</td>';
h+='<td>'+esc(x.published||0)+'</td>';
h+='<td><button class="btn '+(x.enabled?'bad':'ok')+'" onclick="tog(&quot;'+x.id+'&quot;,'+(x.enabled?'false':'true')+')">'+(x.enabled?'Tat':'Bat')+'</button> <button class="btn" onclick="runOne(&quot;'+x.id+'&quot;)">Dang ngay</button></td></tr>'});
h+='</tbody></table></div>';document.getElementById('view').innerHTML=h}
async function ct(){const ch=await api('channels');let opts=(ch.items||[]).map(x=>'<option value="'+x.id+'">'+esc(x.name||x.id)+'</option>').join('');
let h='<div class=panel><h2>Xem noi dung kenh</h2><div class=row><select id=ctCh onchange=ctLoad()>'+opts+'</select></div><div id=ctBody></div></div>';
document.getElementById('view').innerHTML=h;ctLoad()}
async function ctLoad(){const cid=document.getElementById('ctCh').value;const d=await api('channels/'+cid+'/content');
let body='';const it=d.items||{};for(const k in it){const arr=it[k];if(!Array.isArray(arr))continue;
body+='<h3 style="margin:12px 0 6px">'+esc(k)+' ('+arr.length+')</h3><table><thead><tr><th>ID</th><th>Hook</th><th>Trang thai</th></tr></thead><tbody>';
arr.forEach(o=>{body+='<tr><td>'+esc(o.id||'')+'</td><td>'+esc(o.hook||'')+'</td><td>'+(o.published?'<span class="badge b-ok">DA DANG</span>':'<span class="badge b-warn">MOI</span>')+'</td></tr>'});
body+='</tbody></table>'}
document.getElementById('ctBody').innerHTML=body||'<p>Khong co du lieu</p>'}
async function pub(){const ch=await api('channels');let opts=(ch.items||[]).map(x=>'<option value="'+x.id+'">'+esc(x.name||x.id)+'</option>').join('');
let h='<div class=panel><h2>Dang bai thu cong</h2><div class=row><select id=pbCh>'+opts+'</select><input id=pbPer value=2 style=width:60px><button class="btn ok" onclick=pbRun()>Dang</button></div><pre id=pbOut></pre></div>';
document.getElementById('view').innerHTML=h}
async function pbRun(){const cid=document.getElementById('pbCh').value;const per=document.getElementById('pbPer').value;const o=document.getElementById('pbOut');o.textContent='Dang chay...';
try{const r=await fetch('/os/api/channels/'+cid+'/publish?count='+per,{method:'POST'});const d=await r.json();o.textContent=JSON.stringify(d,null,2);toast('Xong','ok')}catch(e){o.textContent='Loi: '+e.message}}
async function runAll(){toast('Dang auto dang tat ca kenh...');
try{const r=await fetch('/os/api/multichannel/run',{method:'POST'});const d=await r.json();toast('Xong','ok');alert(JSON.stringify(d,null,2))}catch(e){toast('Loi: '+e.message,'bad')}}
async function runOne(cid){toast('Dang dang '+cid);
try{const r=await fetch('/os/api/channels/'+cid+'/publish?count=2',{method:'POST'});const d=await r.json();alert(JSON.stringify(d,null,2));toast('Xong','ok')}catch(e){toast('Loi: '+e.message,'bad')}}
async function tog(id,en){await fetch('/os/api/channels/'+id+'/toggle?enabled='+en,{method:'POST'});toast('Da cap nhat '+id,'ok');render()}
async function hist(){const d=await api('videos?limit=40');const items=d.items||[];
let h='<div class=panel><h2>Video da dang gan day</h2><table><thead><tr><th>ID</th><th>Tieu de</th><th>Topic</th><th>YT</th><th>Trang thai</th></tr></thead><tbody>';
items.forEach(v=>{h+='<tr><td>'+esc(v.id)+'</td><td>'+esc((v.title||'').slice(0,60))+'</td><td>'+esc(v.topic||'')+'</td><td>'+(v.youtube_id?'<a style=color:#4f8cff href=https://youtu.be/'+v.youtube_id+' target=_blank>'+v.youtube_id+'</a>':'-')+'</td><td><span class=badge>'+esc(v.status||'')+'</span></td></tr>'});
h+='</tbody></table></div>';document.getElementById('view').innerHTML=h}
async function logs(){const d=await api('agent/actions?limit=40');const items=d.items||[];
let h='<div class=panel><h2>Nhat ky hanh dong agent</h2><table><thead><tr><th>Thoi gian</th><th>Hanh dong</th><th>Chi tiet</th></tr></thead><tbody>';
items.forEach(x=>{h+='<tr><td>'+esc(x.ts)+'</td><td>'+esc(x.action)+'</td><td>'+esc(String(x.detail).slice(0,80))+'</td></tr>'});
h+='</tbody></table></div>';document.getElementById('view').innerHTML=h}
function refresh(){render()}
tabs();render();
