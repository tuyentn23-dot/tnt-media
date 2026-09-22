import sys
sys.path.insert(0, '.')
from ops import channel_loader as ch
try:
	r = ch.create_from_template('whatif_vi', 'What If Viet', 'config/token.pickle')
	sys.stderr.write('OK ' + str(r) + chr(10))
except Exception as e:
	import traceback
	sys.stderr.write('ERR ' + repr(e) + chr(10))
	traceback.print_exc()
