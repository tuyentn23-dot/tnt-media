fn = 'ops/build_gacha_viral.py'
src = open(fn, encoding='utf-8').read()
# Doi PARTS thanh ngan hon (bo tu thua)
old = 'PARTS = ['
# Khong the thay de dang - doc file xem PARTS
idx = src.find('PARTS = [')
print(src[idx:idx+500])