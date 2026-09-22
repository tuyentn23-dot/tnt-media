src = open('ops/ffmpeg_render.py', encoding='utf-8').read()
names = ['def all_dts', 'def drawbar', 'def hook_drawtext', 'def write_chunk_files', 'def split_chunks']
for name in names:
	idx = src.find(name)
	if idx < 0:
		print(name, 'NOT FOUND')
		continue
	end = src.find(chr(10) + 'def ', idx + 5)
	seg = src[idx:end] if end > 0 else src[idx:idx+400]
	print('====', name)
	print(seg[:600])
	print()