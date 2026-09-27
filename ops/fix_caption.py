p = 'ops/ffmpeg_render.py'
b = open(p, 'rb').read()
NL = bytes([10])
T = bytes([9])
# 1. Sua one_dt: them text_align, tang fontsize, doi y
old1 = b":fontsize=52:fontcolor=' + CAP_COLOR + ':borderw=4:bordercolor=black:line_spacing=8'"
new1 = b":fontsize=60:fontcolor=' + CAP_COLOR + ':borderw=5:bordercolor=black:line_spacing=14:text_align=C'"
if old1 in b:
	b = b.replace(old1, new1, 1)
	print('fixed fontsize caption')
else:
	print('NOT FOUND old1')
old2 = b"':x=(w-text_w)/2:y=0.66 * h'"
new2 = b"':x=(w-text_w)/2:y=0.62 * h'"
if old2 in b:
	b = b.replace(old2, new2, 1)
	print('fixed y caption')
else:
	print('NOT FOUND old2')
# 2. Sua hook_drawtext
old3 = b":fontsize=' + str(fs) + ':fontcolor=' + HOOK_COLOR + ':borderw=5:bordercolor=black:line_spacing=12'"
new3 = b":fontsize=' + str(fs) + ':fontcolor=' + HOOK_COLOR + ':borderw=6:bordercolor=black:line_spacing=14:text_align=C'"
if old3 in b:
	b = b.replace(old3, new3, 1)
	print('fixed hook')
else:
	print('NOT FOUND old3')
old4 = b"':x=(w-text_w)/2:y=0.22 * h'"
new4 = b"':x=(w-text_w)/2:y=0.16 * h'"
if old4 in b:
	b = b.replace(old4, new4, 1)
	print('fixed y hook')
else:
	print('NOT FOUND old4')
open(p, 'wb').write(b)
print('done, bytes:', len(b))
