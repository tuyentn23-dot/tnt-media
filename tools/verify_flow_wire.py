import sys, os, json
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from modules.render import video as vid

# Health toan bo
h = vid.health()
print('HEALTH:')
for k, v in h.items():
	print(' ', k, '=', str(v)[:120])

# Build prompt tu item mau
item = {'kind': 'cute_animals', 'topic': 'Meo con ngu tren cua so', 'hook': 'Meo con se lam gi khi troi mua?', 'body': 'Meo con ngu tren cua so khi troi mua'}
style = {'engine': 'flow'}
p = vid.build_prompt(item, style)
print('PROMPT len=', len(p))
print(p[:300])

# Check ENGINES co flow khong
print('ENGINES keys:', list(vid.ENGINES.keys()))
print('flow in ENGINES:', 'flow' in vid.ENGINES)
print('FREE_ENGINES:', vid.FREE_ENGINES)

# Check try_flow importable
import inspect
src = inspect.getsource(vid.try_flow)
print('try_flow signature OK, len:', len(src))
