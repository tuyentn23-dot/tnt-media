from PIL import Image
for f in ['debug_cap5.png', 'debug_cap11.png']:
	im = Image.open('output/' + f)
	w, h = im.size
	yellow = 0
	dark = 0
	for y in range(900, 1090, 4):
		for x in range(80, 640, 8):
			r, g, b = im.getpixel((x, y))
			if r > 200 and g > 180 and b < 120:
				yellow += 1
			if r < 40 and g < 40 and b < 40:
				dark += 1
	print(f, 'yellow:', yellow, 'dark:', dark)