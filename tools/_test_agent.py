import sys
sys.path.insert(0,'.')
from ops import agent_tools as at
print('1. run_cmd:', at.run_cmd('echo hello_agent')['stdout'].strip())
r = at.screenshot()
print('2. screenshot:', r.get('ok'), r.get('path',''))
print('3. actions log:', len(at.list_actions(10)), 'entries')
