import importlib
for m in ['moviepy', 'PIL', 'numpy', 'cv2']:
	try:
		importlib.import_module(m); print(m, 'OK')
	except Exception:
		print(m, 'NO')
