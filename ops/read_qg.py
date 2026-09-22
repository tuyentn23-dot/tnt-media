import os, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = open("ops/quality_gate.py", encoding="utf-8").read()
print(src[600:2500])