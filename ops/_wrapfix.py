import textwrap

def _wrap(dr, text, font, maxw):
 fs = getattr(font, 'size', 40)
 cw = max(6, int(maxw / (fs * 0.5)))
 return textwrap.wrap(text, width=cw) or ['']
