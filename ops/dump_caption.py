src = open('ops/ffmpeg_render.py', encoding='utf-8').read()
names = ['def one_dt', 'def hook_drawtext', 'def write_chunk_files', 'def split_chunks', 'def ffpath', 'def _wrap_text']
out = []
for name in names:
	idx = src.find(name)
	if idx < 0:
		out.append(name + ' MISSING')
		continue
	end = src.find(chr(10) + 'def ', idx + 5)
	seg = src[idx:end] if end > 0 else src[idx:idx+500]
	out.append('==== ' + name + ' ====')
	out.append(seg[:700])
open('output/caption_fns.txt', 'w', encoding='utf-8').write(chr(10).join(out))
print('written', len(out), 'lines')