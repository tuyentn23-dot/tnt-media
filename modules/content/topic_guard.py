# -- coding: utf-8 --
"""Read-only topical guard for channel content before render/publish."""
import unicodedata

MODULE={'name':'content.topic_guard','version':'1.3.2','interface':'check(kind: str, item: dict) -> dict','config_schema':{'kind':'str','item':'dict'},'deps':[],'health':'True'}
CUTE_TERMS=('kitten','kitty','meo','cun','dog','puppy','pet','animal','thu cung','cute','panda','rabbit','bunny','hamster','otter')
BLOCK_TERMS=('iran','military','war','missile','pentagon','conflict','attack','aircraft loss','chien tranh','quan su','ten lua','xung dot','tong bi thu','chu tich nuoc','doi ngoai','my','canada','chinh tri','government','president','election','tau ngam','trung quoc','ukraine','nga','donetsk')

def norm(value):
 raw=unicodedata.normalize('NFKD',str(value or '')).encode('ascii','ignore').decode('ascii').lower()
 clean=''.join(ch if ch.isalnum() else ' ' for ch in raw)
 return ' '.join(clean.split())

def term_match(text,term):
 t=norm(term)
 return bool(t) and (' '+t+' ') in (' '+text+' ')

def check(kind,item):
 text=norm(' '.join(str(item.get(k) or '') for k in ('hook','body','payoff')))
 item_id=str(item.get('id') or '')
 blocked=[x for x in BLOCK_TERMS if term_match(text,x)]
 cute_hits=[x for x in CUTE_TERMS if term_match(text,x)]
 is_cute=(kind=='cute_animals')
 live_source_mismatch=is_cute and item_id.startswith('live_cute_animals_')
 allowed=(bool(cute_hits) and not blocked and not live_source_mismatch) if is_cute else (not blocked)
 reason=('live_source_mismatch' if live_source_mismatch else ('cute_signal_present' if allowed else ('blocked_unrelated_news' if blocked else 'missing_cute_animal_signal'))) if is_cute else ('allowed' if allowed else 'blocked_sensitive_news')
 return {'allowed':allowed,'reason':reason,'kind':kind,'cute_hits':cute_hits[:5],'blocked_hits':blocked[:5]}

def filter_items(kind,items):
 return [item for item in items if check(kind,item)['allowed']]

def health():
 return True
