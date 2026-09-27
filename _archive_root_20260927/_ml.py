import sys, os, asyncio, edge_tts
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
async def go(v, out):
	c = edge_tts.Communicate('Con bạch tuộc có 3 trái tim và máu màu xanh', v)
	await c.save(out)
for v in ['en-US-AvaMultilingualNeural', 'en-US-EmmaMultilingualNeural', 'en-US-BrianMultilingualNeural']:
	try:
		asyncio.run(go(v, 'output/ml' + v.split('-')[2][:5] + '.mp3'))
		print(v, 'OK')
	except Exception as e:
		print(v, 'FAIL' , str(e)[:50])
