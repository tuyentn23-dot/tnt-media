import importlib
def chk(m):
	try:
		importlib.import_module(m)
		return m + ' OK'
	except Exception:
		return m + ' MISSING'
for m in ['whisper', 'faster_whisper', 'vosk', 'speech_recognition']:
	print(chk(m))
