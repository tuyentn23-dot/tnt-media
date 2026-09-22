from PIL import Image
import os
d = 'output/CHECK'
files = sorted([f for f in os.listdir(d) if f.startswith('anime_final_')])
print('files:', len(files))
im1 = Image.open(os.path.join(d, 'anime_final_0_0.png'))
im2 = Image.open(os.path.join(d, 'anime_final_0_3.png'))
im3 = Image.open(os.path.join(d, 'anime_final_1_0.png'))
im4 = Image.open(os.path.join(d, 'anime_final_2_0.png'))
w, h = im1.size
diff_a = 0
for y in range(0, h, 30):
	for x in range(0, w, 30):
		if im1.getpixel((x, y)) != im2.getpixel((x, y)):
			diff_a += 1
print('anim diff t=0 vs t=4.5:', diff_a)
diff_b = 0
for y in range(0, h, 30):
	for x in range(0, w, 30):
		if im1.getpixel((x, y)) != im3.getpixel((x, y)):
			diff_b += 1
print('palette diff pal0 vs pal1:', diff_b)
yy = int(h * 0.15)
print('pal0 upper:', im1.getpixel((w // 2, yy)))
print('pal1 upper:', im3.getpixel((w // 2, yy)))
print('pal2 upper:', im4.getpixel((w // 2, yy)))