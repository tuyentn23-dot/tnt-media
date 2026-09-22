import os, subprocess
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
frames = os.path.abspath(os.path.join('output', 'frames_tmp', 'f%04d.png'))
music = os.path.abspath(os.path.join('assets', 'music_clips', 'clip_0_0.mp3'))
final = os.path.abspath(os.path.join('output', 'CHECK', 'gacha_clip.mp4'))
os.makedirs(os.path.dirname(final), exist_ok=True)
cmd = [FFMPEG, '-y', '-framerate', '6', '-i', frames, '-i', music, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-c:a', 'aac', '-b:a', '192k', '-shortest', final]
r = subprocess.run(cmd, capture_output=True, text=True)
print('rc:', r.returncode)
if r.returncode != 0:
	print(r.stderr[-800:])
print('size:', os.path.getsize(final) if os.path.exists(final) else 0)