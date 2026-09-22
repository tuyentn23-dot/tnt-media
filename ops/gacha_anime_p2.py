# gacha_anime_p2.py - phan 2: ve toc bang BEZIER PATH
import math, random
from math import comb
from PIL import Image, ImageDraw

def bezier(pts, steps=24):
	n = len(pts) - 1
	out = []
	for i in range(steps + 1):
		t = i / steps
		x = 0.0
		y = 0.0
		for k in range(len(pts)):
			px, py = pts[k]
			b = comb(n, k) * (t ** k) * ((1 - t) ** (n - k))
			x += px * b
			y += py * b
		out.append((x, y))
	return out

def draw_path(dr, pts, width, fill, steps=24):
	pts2 = bezier(pts, steps)
	dr.line(pts2, fill=fill, width=width, joint='curve')
	r = max(1, width // 2)
	dr.ellipse([pts2[0][0] - r, pts2[0][1] - r, pts2[0][0] + r, pts2[0][1] + r], fill=fill)
	dr.ellipse([pts2[-1][0] - r, pts2[-1][1] - r, pts2[-1][0] + r, pts2[-1][1] + r], fill=fill)
	return pts2
