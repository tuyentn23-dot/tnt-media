from PIL import Image
im = Image.open('output/verify_last.png')
w, h = im.size
print('size:', im.size)
# Kiem tra vung caption (y=880..1100)
white_px = 0
pink_border = 0
for y in range(880, 1100, 4):
	for x in range(80, 640, 6):
		r, g, b = im.getpixel((x, y))
		if r > 230 and g > 230 and b > 230:
			white_px += 1
		if r > 230 and g < 100 and 100 < b < 200:
			pink_border += 1
print('white (chu):', white_px)
print('pink (vien):', pink_border)
# Check nhan vat
print('char mid:', im.getpixel((w // 2, h // 2)))