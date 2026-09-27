import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
L = open(p, encoding='utf-8').read().split(NL)
for i, l in enumerate(L):
 if 'height=1920' in l and 'cropped' in l:
 L[i] = T + 'b = (b.cropped(width=720, height=1280, x_center=b.w / 2, y_center=b.h / 2) if hasattr(b, ' + DQ + 'cropped' + DQ + ') else b.crop(x1=(b.w-720)//2, y1=(b.h-1280)//2, width=720, height=1280))'
 print('fixed 70', i + 1)
start = None
end = None
for i, l in enumerate(L):
 if 'ov' + U + 'f = (overlay.astype' in l:
 start = i
 if 'return out.astype(' + DQ + 'uint8' + DQ + ')' in l and start is not None:
 end = i
 break
print('composite block:', start + 1, '-', end + 1 if end else 'NOT FOUND')
if start is not None and end is not None:
 new_block = [
 T + 'def mk(get, t):',
 T + T + 'from PIL import Image',
 T + T + 'fr = get(t)',
 T + T + 'base = Image.fromarray(fr.astype(' + DQ + 'uint8' + DQ + ')).convert(' + DQ + 'RGBA' + DQ + ')',
 T + T + 'base.alpha' + U + 'composite(overlay)',
 T + T + 'return base.convert(' + DQ + 'RGB' + DQ + ').' + U + U + 'array' + U + U + '()',
 ]
 L = L[:start] + new_block + L[end + 1:]
 content = NL.join(L)
 open(p, 'w', encoding='utf-8').write(content)
 try:
 ast.parse(content)
 print('PIL PATCH OK, lines:', len(L))
 except Exception as e:
 print('ERR:', e)
 for j in range(start - 2, start + 10):
 print(j + 1, repr(L[j])[:140])
