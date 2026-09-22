# caption_styles.py - 4 style caption khac nhau cho tung video
# 1. meme - vang vien den, font Segoe (meme classic)
# 2. cute - trang vien hong, font Tahoma (kawaii)
# 3. cool - xanh neon vien den, font Calibri (gaming)
# 4. dramatic - trang vien do, font Segoe (emotion)
STYLES = {
	"meme": {
		"font": "tools/font_segoe_bold.ttf",
		"size": 58,
		"color": "0xFFEB3B",
		"border": 6,
		"bcolor": "0x000000",
		"shadow": 4,
		"scolor": "0x000000@0.9"
	},
	"cute": {
		"font": "tools/font_tahoma_bold.ttf",
		"size": 56,
		"color": "0xFFFFFF",
		"border": 6,
		"bcolor": "0xFF1493",
		"shadow": 4,
		"scolor": "0x000000@0.9"
	},
	"cool": {
		"font": "tools/font_calibri_bold.ttf",
		"size": 60,
		"color": "0x00FFFF",
		"border": 5,
		"bcolor": "0x000000",
		"shadow": 5,
		"scolor": "0x000000@0.95"
	},
	"dramatic": {
		"font": "tools/font_segoe_bold.ttf",
		"size": 56,
		"color": "0xFFFFFF",
		"border": 7,
		"bcolor": "0xCC0000",
		"shadow": 5,
		"scolor": "0x000000@0.95"
	}
}

def build_dt(fp, a, b, style):
	st = STYLES.get(style, STYLES["meme"])
	en = "between(t," + str(round(a, 2)) + "," + str(round(b + 0.1, 2)) + ")"
	qt = chr(39)
	s = "drawtext=fontfile=" + st["font"] + ":textfile=" + fp + ":enable=" + qt + en + qt
	s += ":fontsize=" + str(st["size"])
	s += ":fontcolor=" + st["color"]
	s += ":borderw=" + str(st["border"]) + ":bordercolor=" + st["bcolor"]
	s += ":shadowx=" + str(st["shadow"]) + ":shadowy=" + str(st["shadow"]) + ":shadowcolor=" + st["scolor"]
	s += ":line_spacing=12:x=(w-text_w)/2:y=h-380"
	return s