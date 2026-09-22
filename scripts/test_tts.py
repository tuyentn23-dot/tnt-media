import asyncio, edge_tts
async def main():
	text = 'Meo con de thuong qua! Cac ban thay the nao?'
	comm = edge_tts.Communicate(text, 'vi-VN-HoaiMyNeural')
	await comm.save('output/music/test_voice.mp3')
	print('SAVED VOICE')
asyncio.run(main())
