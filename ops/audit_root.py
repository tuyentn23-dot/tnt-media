import os, json
R = os.getcwd()
F = sorted(f for f in os.listdir(R) if os.path.isfile(os.path.join(R, f)))
D = sorted(d for d in os.listdir(R) if os.path.isdir(os.path.join(R, d)))
isTmp = lambda f: "TEMP" in f.upper() or ".bak" in f or f.startswith("chunk")
J = [f for f in F if isTmp(f)]
K = [f for f in F if not isTmp(f)]
print("FILES: