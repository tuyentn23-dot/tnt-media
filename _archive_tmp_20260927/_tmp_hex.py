import base64,sys
p=sys.argv[1] if len(sys.argv)>1 else '_serve.py'
b=open(p,'rb').read()[:400]
print(base64.b64encode(b).decode())
