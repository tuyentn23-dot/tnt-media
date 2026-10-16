# -- coding: utf-8 --
# desktop_app/tokens.py - Design tokens (iOS HIG inspired)

def _rgb(h):
	h = h.lstrip('#')
	return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

LIGHT = {
	# Surfaces
	'bg': '#F2F2F7',
	'bg_grouped': '#F2F2F7',
	'surface': '#FFFFFF',
	'surface_alt': '#FAFAFC',
	'sidebar': '#ECECEE',
	'sidebar_sel': '#DCEBFF',
	'sep': '#E5E5EA',
	'sep_strong': '#D1D1D6',
	# Labels
	'label': '#1C1C1E',
	'label2': '#3A3A3C',
	'label3': '#8E8E93',
	'label4': '#C7C7CC',
	# Accent
	'accent': '#0A84FF',
	'accent_hover': '#0070E0',
	'accent_soft': '#E5F0FF',
	'accent_text': '#0A84FF',
	# Semantic
	'green': '#34C759',
	'red': '#FF3B30',
	'orange': '#FF9500',
	'purple': '#AF52DE',
	'pink': '#FF375F',
	'teal': '#30B0C7',
	# Controls
	'ctrl_bg': '#FFFFFF',
	'ctrl_border': '#D1D1D6',
	'ctrl_hover': '#F0F0F2',
	'row_hover': '#F5F5F7',
	'sel_bg': '#D6E9FF',
	'sel_fg': '#1C1C1E',
	# Shadow
	'shadow': 'rgba(0,0,0,0.06)',
}

DARK = {
	'bg': '#1C1C1E',
	'bg_grouped': '#000000',
	'surface': '#2C2C2E',
	'surface_alt': '#242426',
	'sidebar': '#252527',
	'sidebar_sel': '#0A3A6B',
	'sep': '#38383A',
	'sep_strong': '#48484A',
	'label': '#F2F2F7',
	'label2': '#D1D1D6',
	'label3': '#8E8E93',
	'label4': '#5A5A5E',
	'accent': '#0A84FF',
	'accent_hover': '#3A9BFF',
	'accent_soft': '#0A2A4A',
	'accent_text': '#5AC8FA',
	'green': '#30D158',
	'red': '#FF453A',
	'orange': '#FF9F0A',
	'purple': '#BF5AF2',
	'pink': '#FF375F',
	'teal': '#40C8E0',
	'ctrl_bg': '#2C2C2E',
	'ctrl_border': '#48484A',
	'ctrl_hover': '#3A3A3C',
	'row_hover': '#2C2C2E',
	'sel_bg': '#0A3A6B',
	'sel_fg': '#FFFFFF',
	'shadow': 'rgba(0,0,0,0.35)',
}

SPACE = {'xs': 4, 'sm': 8, 'md': 12, 'lg': 16, 'xl': 24, 'xxl': 32}
RADIUS = {'sm': 6, 'md': 8, 'lg': 12, 'xl': 16, 'pill': 999}

def palette(theme='light'):
	return DARK if theme == 'dark' else LIGHT
