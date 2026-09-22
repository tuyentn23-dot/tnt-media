import sys
sys.path.insert(0, '.')
from ops.youtube_uploader import get_authenticated_service
s = get_authenticated_service()
for v in ['eybQ5ZKotOY', 'aAYGoWL2ZMo']:
	try:
		s.videos().delete(id=v).execute()
		print('DELETED', v)
	except Exception as e:
		print('ERR', v, str(e)[:100])
