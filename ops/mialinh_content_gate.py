# -- coding: utf-8 --
"""Pre-render script gate for Mialinhcute. This is a structural proxy, not a prediction of views."""

ACTION_WORDS=('bỗng','chạy','rơi','mất','phát hiện','nghe','thấy','mở','cứu','đuổi','trốn','biến mất','xuất hiện')
TWIST_WORDS=('nhưng','hóa ra','không ngờ','bất ngờ','thật ra','đột nhiên','cuối cùng')

_text=lambda item,key: str(item.get(key) or '').strip()
_has=lambda text,words: any(w in text.lower() for w in words)

_base=lambda item: (_text(item,'hook'),_text(item,'body'),_text(item,'payoff'),_text(item,'question'))
_parts=lambda h,b,p,q: {'hook':25 if 8<=len(h)<=80 else (12 if h else 0),'action':20 if _has(' '.join((h,b,p)),ACTION_WORDS) else 0,'twist':20 if _has(' '.join((h,b,p)),TWIST_WORDS) else 0,'payoff':20 if 8<=len(p)<=140 else (8 if p else 0),'clarity':10 if 20<=len(' '.join((h,b,p)))<=420 else 4,'question':5 if q else 0}
_fact=lambda h,parts: any(x in h.lower() for x in (' là ',' có ',' được ',' thuộc ',' gọi là ')) and parts['action']==0
_make=lambda h,b,p,q,parts,fact: {'score':min(55,sum(parts.values())) if fact else min(100,sum(parts.values())),'passes':(min(55,sum(parts.values())) if fact else min(100,sum(parts.values())))>=70 and not fact and parts['action']>0 and parts['twist']>0 and parts['payoff']>=15,'parts':parts,'reasons':([] if parts['hook']>=20 else ['hook_weak'])+([] if parts['action'] else ['no_action'])+([] if parts['twist'] else ['no_twist'])+([] if parts['payoff']>=15 else ['payoff_weak'])+(['fact_only_hook'] if fact else []),'score_kind':'script_structure_proxy'}
_score_struct=lambda item: (lambda vals:(lambda parts:_make(vals[0],vals[1],vals[2],vals[3],parts,_fact(vals[0],parts)))(_parts(*vals)))(_base(item))
score=lambda item: {'score':0,'passes':False,'parts':{},'reasons':['copyrighted_ip_risk'],'score_kind':'script_structure_proxy'} if str(item.get('topic') or item.get('_bucket') or '').strip().lower() in ('anime','roblox','gacha') else _score_struct(item)
