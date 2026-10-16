# -- coding: utf-8 --
import os
import style_build

ACCENT = '#0A84FF'

def stylesheet(theme='light'):
	try:
		return style_build.build(theme)
	except Exception:
		return ''
