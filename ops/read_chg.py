import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
src = open("CHANGELOG.md", encoding="utf-8").read()
print(src[400:1527])