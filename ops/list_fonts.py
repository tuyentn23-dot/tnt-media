import os, glob
out = []
if os.path.isdir('tools'):
	for f in os.listdir('tools'):
		if f.endswith('.ttf') or f.endswith('.otf'):
			p = os.path.join('tools', f)
			out.append('tool: ' + f + ' ' + str(os.path.getsize(p)))
for f in glob.glob('C:/Windows/Fonts/*.ttf')[:40]:
	out.append('sys: ' + os.path.basename(f))
open('output/fonts_list.txt', 'w', encoding='utf-8').write(chr(10).join(out))
print('written', len(out))