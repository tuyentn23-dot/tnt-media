# Xem cach ffmpeg_render escape path ffmpeg
src = open('ops/ffmpeg_render.py', encoding='utf-8').read()
idx = src.find('def ffpath')
end = src.find(chr(10) + 'def ', idx + 5)
print(src[idx:end])