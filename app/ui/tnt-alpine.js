(function(){
function reactive(obj, render){ return new Proxy(obj, { set(t,k,v){ t[k]=v; render(); return true; }, get(t,k){ return t[k]; } }); }
function evalIn(scope, expr){ try { return Function('s','with(s){return ('+expr+')}')(scope); } catch(e){ return undefined; } }
function runIn(scope, expr){ try { Function('s','with(s){'+expr+'}')(scope); } catch(e){} }
function setPath(scope, path, val){ try { Function('s','v','with(s){'+path+'=v}')(scope, val); } catch(e){} }
function applyDirectives(el, scope){
if (el.hasAttribute('x-show')){ el.style.display = evalIn(scope, el.getAttribute('x-show')) ? '' : 'none'; }
if (el.hasAttribute('x-text')){ var tv = evalIn(scope, el.getAttribute('x-text')); el.textContent = (tv===undefined||tv===null) ? '' : tv; }
if (el.hasAttribute('x-model')){ var mp = el.getAttribute('x-model'); var mv = evalIn(scope, mp); if (el.type==='checkbox') el.checked = !!mv; else el.value = (mv===undefined?'':mv); el.oninput = function(){ setPath(scope, mp, el.type==='checkbox'?el.checked:el.value); }; }
var ck = el.getAttribute('@click');
if (ck && !el.__bound){ el._bound = true; el.addEventListener('click', function(ev){ ev.preventDefault(); runIn(scope, ck); }); }
var cc = el.getAttribute(':class');
if (cc){ var cv = evalIn(scope, cc); if (typeof cv === 'string') el.className = cv; }
}
function walk(node, scope){ var c = node.firstElementChild; while(c){ applyDirectives(c, scope); walk(c, scope); c = c.nextElementSibling; } }
function renderFor(el, scope){
var expr = el.getAttribute('x-for'); var m = expr.match(/^\s*([A-Za-z0-9]+)\s+in\s+(.+)/); if(!m) return;
var itemName = m[1], listExpr = m[2]; var arr = evalIn(scope, listExpr) || []; var parent = el.parentNode;
if (!el.__tpl){ el.__tpl = el.cloneNode(true); el.__tpl.removeAttribute('x-for'); }
if (!el.__marker){ el.__marker = document.createComment('x-for'); }
if (!el.__marker.parentNode){ parent.insertBefore(el.__marker, el); }
var cursor = el.__marker.nextSibling;
var olds = []; var n = cursor; while(n && n !== el){ olds.push(n); n = n.nextSibling; }
olds.forEach(function(x){ x.remove(); });
arr.forEach(function(item, i){
var node = el.__tpl.cloneNode(true); var cs = Object.create(scope); cs[itemName] = item; cs.$index = i;
applyDirectives(node, cs); walk(node, cs); parent.insertBefore(node, cursor);
});
}
function bind(root){
var dataExpr = root.getAttribute('x-data') || '{}'; var base;
try { base = Function('return ('+dataExpr+')')(); } catch(e){ base = {}; }
var scope = reactive(base, function(){ walk(root, scope); });
root.__scope = scope; walk(root, scope);
var initExpr = root.getAttribute('x-init');
if (initExpr){ Promise.resolve(runIn(scope, initExpr)); }
}
window.Alpine = { start: function(){ document.querySelectorAll('[x-data]').forEach(bind); } };
document.addEventListener('DOMContentLoaded', function(){ window.Alpine.start(); });
})();
