import os, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
mv = os.path.abspath('output/CHECK/anime_mv_test.mp4')
vo = os.path.abspath('output/ai_vo_crush.mp3')
music = os.path.abspath('assets/music_clips/clip_0_0.mp3')
final = os.path.abspath('output/Mialinhcute_gacha_ai.mp4')
cmd = [FFMPEG, '-y', '-i', mv, '-i', vo, '-i', music, '-filter_complex', '[1:a]volume=1.6[a1];[2:a]volume=0.25[a2];[a1][a2]amix=inputs=2:duration=longest[aout]', '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', final]
r = subprocess.run(cmd, capture_output=True, text=True)
print('rc:', r.returncode)
if r.returncode != 0:
	print(r.stderr[-600:])
print('final size:', os.path.getsize(final) if os.path.exists(final) else 0)