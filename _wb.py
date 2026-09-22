import asyncio, edge_tts, json
async def go():
	c = edge_tts.Communicate('Xin chao cac ban day la thu nghiem', 'vi-VN-HoaiMyNeural')
	words = []
	async for ch in c.stream():
		if ch['type'] == 'WordBoundary':
			words.append((ch['text'], round(ch['offset']/10000000, 2), round(ch['duration']/10000000, 2)))
	return words
w = asyncio.run(go())
print(json.dumps(w, ensure_ascii=False)[:600])
