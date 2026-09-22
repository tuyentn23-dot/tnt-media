import os, sys, subprocess, importlib
try:
	r = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], capture_output=True, text=True, timeout=10)
	print('GPU:', r.stdout.strip()[:300])
except Exception as e:
	print('wmic err', str(e)[:80])
mods = ['torch', 'diffusers', 'transformers', 'accelerate', 'safetensors', 'onnxruntime', 'cv2', 'requests', 'openai', 'huggingface_hub']
for m in mods:
	try:
		importlib.import_module(m)
		print('OK ', m)
	except Exception as e:
		print('NO ', m)