from PIL import Image
import os
files = sorted([f for f in os.listdir('output/gacha_char') if f.startswith('pose')])
for f in files:
	im = Image.open('output/gacha_char/' + f)
	w, h = im.size
	print(f, im.size, 'top:', im.getpixel((w // 2, h // 4)), 'mid:', im.getpixel((w // 2, h // 2)), 'bot:', im.getpixel((w // 2, 3 * h // 4)))