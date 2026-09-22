import importlib
def chk(m):
	try:
		importlib.import_module(m)
		return m + ' OK'
	except Exception:
		return m + ' NO'
for m in ['cv2', 'rembg', 'PIL', 'moviepy', 'imageio', 'scipy', 'skimage']:
	print(chk(m))
