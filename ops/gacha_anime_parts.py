# gacha_anime_parts.py - ve cac bo phan chi tiet: mat, mieng, ngon tay, nep ao
import math
from PIL import ImageDraw

# ---- MAT ----
def draw_eyes(dr, head, r, eye_color, openness=1.0, look=0.0):
	hx, hy = head
	y = hy + r * 0.05
	o = max(0.05, openness)
	for s in (-1, 1):
		ex = hx + s * r * 0.26
		# long trang
		dr.ellipse([ex - r * 0.17, y - r * 0.16 * o, ex + r * 0.17, y + r * 0.24 * o], fill=(255, 255, 255))
		# long den gradient (nhieu lop)
		cx_eye = ex + look * r * 0.04
		dr.ellipse([cx_eye - r * 0.12, y - r * 0.10 * o, cx_eye + r * 0.12, y + r * 0.18 * o], fill=(80, 60, 130))
		dr.ellipse([cx_eye - r * 0.09, y - r * 0.06 * o, cx_eye + r * 0.09, y + r * 0.12 * o], fill=eye_color)
		# highlight 2 dom
		dr.ellipse([cx_eye - r * 0.06, y - r * 0.08 * o, cx_eye + r * 0.01, y - r * 0.01 * o], fill=(255, 255, 255))
		dr.ellipse([cx_eye + r * 0.03, y + r * 0.05 * o, cx_eye + r * 0.07, y + r * 0.10 * o], fill=(255, 255, 255, 200))
		# mi tren (path day)
		dr.line([(ex - r * 0.2, y - r * 0.2 * o), (ex, y - r * 0.26 * o), (ex + r * 0.2, y - r * 0.2 * o)], fill=(60, 40, 90), width=3)


def draw_mouth(dr, head, r, open_amt=0.5, smile=0.0):
	hx, hy = head
	my = hy + r * 0.55
	ow = r * 0.10
	if open_amt < 0.15:
		# mieng dong: duong cong nhe
		dr.line([(hx - ow, my + smile * r * 0.02), (hx, my + r * 0.04 + smile * r * 0.02), (hx + ow, my + smile * r * 0.02)], fill=(200, 70, 100), width=3)
	else:
		oh = r * 0.16 * open_amt
		dr.ellipse([hx - ow, my - oh * 0.3, hx + ow, my + oh], fill=(210, 70, 100))
		dr.ellipse([hx - ow * 0.6, my + oh * 0.1, hx + ow * 0.6, my + oh * 0.5], fill=(240, 130, 150))


def draw_blush(dr, head, r, alpha_color=(255, 160, 180)):
	hx, hy = head
	y = hy + r * 0.35
	for s in (-1, 1):
		bx = hx + s * r * 0.5
		dr.ellipse([bx - r * 0.12, y - r * 0.05, bx + r * 0.12, y + r * 0.07], fill=alpha_color)


# ---- NGON TAY ----
def draw_hand(dr, wrist, elbow, r, skin, spread=1.0):
	wx, wy = wrist
	ex, ey = elbow
	# huong tu elbow -> wrist
	dx, dy = wx - ex, wy - ey
	d = math.hypot(dx, dy) or 1
	ux, uy = dx / d, dy / d
	# vector vuong goc
	px, py = -uy, ux
	# ve ban tay (hinh oval nho)
	hw = r * 0.09 * spread
	hh = r * 0.13
	dr.ellipse([wx - hw, wy - hh, wx + hw, wy + hh], fill=skin)
	# 4 ngon tay xoe ra tu ban tay theo huong u
	for i in range(4):
		off = (i - 1.5) * r * 0.05 * spread
		bx = wx + ux * r * 0.05 + px * off
		by = wy + uy * r * 0.05 + py * off
		tx = bx + ux * r * 0.10
		ty = by + uy * r * 0.10
		dr.line([(bx, by), (tx, ty)], fill=skin, width=max(3, int(r * 0.03)))
		rr = max(2, int(r * 0.018))
		dr.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=skin)


# ---- NEP AO ----
def draw_folds(dr, sh_l, sh_r, hip_l, hip_r, top_color):
	dark = tuple(max(0, int(v * 0.82)) for v in top_color)
	# 2 duong cheo tu vai xuong hong
	mx_l = ((sh_l[0] + hip_l[0]) / 2, (sh_l[1] + hip_l[1]) / 2)
	mx_r = ((sh_r[0] + hip_r[0]) / 2, (sh_r[1] + hip_r[1]) / 2)
	dr.line([mx_l, (sh_l[0] * 0.3 + hip_l[0] * 0.7, sh_l[1] * 0.3 + hip_l[1] * 0.7)], fill=dark, width=3)
	dr.line([mx_r, (sh_r[0] * 0.3 + hip_r[0] * 0.7, sh_r[1] * 0.3 + hip_r[1] * 0.7)], fill=dark, width=3)
	# 1 duong ngang eo
	dr.line([(sh_l[0] * 0.35 + hip_l[0] * 0.65, sh_l[1] * 0.35 + hip_l[1] * 0.65), (sh_r[0] * 0.35 + hip_r[0] * 0.65, sh_r[1] * 0.35 + hip_r[1] * 0.65)], fill=dark, width=2)
