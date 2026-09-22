# gacha_anime_p3.py - phan 3: ve TOC bang bezier path (nhieu lop)
import math

# shape toc: tra ve list cac path (moi path = list control points)
def hair_paths(cx, cy, r, style='long'):
	paths = []
	# lop toc mai (top) - tu dinh dau vuot xuong 2 ben
	# control points: dinh trai, dinh phai, vai trai, vai phai
	top_left = [
		(cx - r * 0.1, cy - r * 1.05),
		(cx - r * 0.75, cy - r * 1.0),
		(cx - r * 1.05, cy - r * 0.3),
		(cx - r * 1.0, cy + r * 0.4),
		(cx - r * 0.85, cy + r * 0.85),
	]
	top_right = [
		(cx + r * 0.1, cy - r * 1.05),
		(cx + r * 0.75, cy - r * 1.0),
		(cx + r * 1.05, cy - r * 0.3),
		(cx + r * 1.0, cy + r * 0.4),
		(cx + r * 0.85, cy + r * 0.85),
	]
	paths.append(('main', top_left))
	paths.append(('main', top_right))
	# mai toc (fringe) - nhieu soi roi xuong tra
	for i in range(5):
		t = (i + 0.5) / 5.0
		fx = cx + (t - 0.5) * r * 1.4
		tip_x = cx + (t - 0.5) * r * 1.5 + math.sin(i) * r * 0.1
		fringe = [
			(fx, cy - r * 0.95),
			(fx + (tip_x - fx) * 0.4, cy - r * 0.55),
			(fx + (tip_x - fx) * 0.8, cy - r * 0.15),
			(tip_x, cy + r * 0.05),
		]
		paths.append(('fringe', fringe))
	if style == 'long':
		# toc dai sau lung
		back_left = [
			(cx - r * 0.9, cy + r * 0.6),
			(cx - r * 1.15, cy + r * 1.6),
			(cx - r * 1.1, cy + r * 2.6),
			(cx - r * 0.7, cy + r * 3.2),
		]
		back_right = [
			(cx + r * 0.9, cy + r * 0.6),
			(cx + r * 1.15, cy + r * 1.6),
			(cx + r * 1.1, cy + r * 2.6),
			(cx + r * 0.7, cy + r * 3.2),
		]
		paths.append(('back', back_left))
		paths.append(('back', back_right))
	return paths
