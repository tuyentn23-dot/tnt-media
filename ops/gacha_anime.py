# gacha_anime.py - anime gacha voi SKELETON + BEZIER PATH
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
S = 4
W, H = 720 * S, 1280 * S

def _c(x):
	return tuple(max(0, min(255, int(v))) for v in x)

def _shade(c, f):
	return _c(tuple(v * f for v in c))

def skeleton(cx, cy, r, t=0.0):
	bob = math.sin(t * 2.2) * r * 0.02
	sway = math.sin(t * 1.4) * r * 0.015
	j = {}
	j['head'] = (cx + sway, cy + bob)
	j['neck'] = (cx + sway * 0.6, cy + r * 0.95 + bob)
	j['shoulder_l'] = (cx - r * 0.52 + sway * 0.4, cy + r * 1.18 + bob)
	j['shoulder_r'] = (cx + r * 0.52 + sway * 0.4, cy + r * 1.18 + bob)
	j['elbow_l'] = (cx - r * 0.68 + sway * 0.3, cy + r * 1.62 + bob * 0.7)
	j['elbow_r'] = (cx + r * 0.68 + sway * 0.3, cy + r * 1.62 + bob * 0.7)
	j['wrist_l'] = (cx - r * 0.72 + sway * 0.2, cy + r * 2.02 + bob * 0.5)
	j['wrist_r'] = (cx + r * 0.72 + sway * 0.2, cy + r * 2.02 + bob * 0.5)
	j['hip_l'] = (cx - r * 0.22 + sway * 0.15, cy + r * 2.0 + bob * 0.8)
	j['hip_r'] = (cx + r * 0.22 + sway * 0.15, cy + r * 2.0 + bob * 0.8)
	j['knee_l'] = (cx - r * 0.24 + sway * 0.1, cy + r * 2.55 + bob * 0.6)
	j['knee_r'] = (cx + r * 0.24 + sway * 0.1, cy + r * 2.55 + bob * 0.6)
	j['ankle_l'] = (cx - r * 0.26, cy + r * 3.05 + bob * 0.4)
	j['ankle_r'] = (cx + r * 0.26, cy + r * 3.05 + bob * 0.4)
	j['r'] = r
	return j
