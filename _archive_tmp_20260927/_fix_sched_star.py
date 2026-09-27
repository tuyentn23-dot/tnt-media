import ast
U = chr(95) + chr(95)
Q = chr(39)
STAR = chr(42)
SLASH = chr(47)
p = 'pipeline/scheduler.py'
src = open(p, encoding='utf-8').read()

# Fix field == '' -> field == ''
old1 = 'if field == ' + Q + Q + ':'
new1 = 'if field == ' + Q + STAR + Q + ':'
src = src.replace(old1, new1)

# Fix part == '' -> part == ''
old2 = "if part == " + Q + Q + ":"
new2 = "if part == " + Q + STAR + Q + ":"
src = src.replace(old2, new2)

# Fix '/' in part if stripped
old3 = 'if ' + Q + Q + ' in part:'
new3 = 'if ' + Q + SLASH + Q + ' in part:'
src = src.replace(old3, new3)

# Fix split('/', 1) if stripped
old4 = "base, sp = part.split(" + Q + Q + 