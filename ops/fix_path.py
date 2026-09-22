fn = 'ops/build_pika_mv2.py'
src = open(fn, encoding='utf-8').read()
# 1. Doi FONT thanh relative
old1 = chr(70) + 'ONT = os.path.abspath(os.path.join(' + chr(39) + 'tools' + chr(39) + ', ' + chr(39) + 'font_black.ttf' + chr(39) + '))'
new1 = chr(70) + 'ONT = ' + chr(39) + 'tools/font_black.ttf' + chr(39)
c1 = src.count(old1)
src = src.replace(old1, new1)
print('FONT replaced:', c1)
# 2. Doi dong ff = ... thanh ff = FONT
old2 = chr(39) + 'ff = FONT.replace(chr(92), chr(47))' + chr(39)
new2 = chr(39) + 'ff = FONT' + chr(39)
c2 = src.count(old2)
src = src.replace(old2, new2)
print('ff replaced:', c2)
open(fn, 'w', encoding='utf-8').write(src)
print('done')