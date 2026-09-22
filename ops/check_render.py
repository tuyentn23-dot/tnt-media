from PIL import Image
im = Image.open('output/CHECK/anime_test_0.png')
print('size:', im.size, 'mode:', im.mode)
w, h = im.size
samples = {}
samples['top'] = im.getpixel((w // 2, 20))
samples['upper'] = im.getpixel((w // 2, int(h * 0.15)))
samples['center'] = im.getpixel((w // 2, int(h * 0.45)))
samples['lower'] = im.getpixel((w // 2, int(h * 0.85)))
for k, v in samples.items():
	print(k, v)
im2 = Image.open('output/CHECK/anime_test_2.png')
diff = 0
for y in range(0, h, 50):
	for x in range(0, w, 50):
		if im.getpixel((x, y)) != im2.getpixel((x, y)):
			diff += 1
print('diff pixels (sampled):', diff)
