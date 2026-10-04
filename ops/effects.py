# -- coding: utf-8 --
# Effects: hook text + CTA cho Shorts
import os, subprocess, re

def _ff():
	root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	ff = os.path.join(root, 'tools', 'ffmpeg.exe')
	return ff if os.path.exists(ff) else 'ffmpeg'

def _dur(path):
	r = subprocess.run([_ff(), '-i', path, '-hide_banner'], capture_output=True, text=True)
	m = re.search('Duration: ([0-9]+):([0-9]+):([0-9.]+)', r.stderr)
	if not m:
		return 0.0
	return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))

def hook_text(path, text, duration=2.5, fontsize=72, y_frac=0.15):
	tmp = path + '.hook.mp4'
	safe = text.replace(':', '').replace('', '')
	safe = safe.replace(chr(37), chr(37) + chr(37))
	Q2 = chr(39)
	alpha = 'if(lt(t,0.5),t/0.5,1)'
	ypos = 'h*' + str(y_frac)
	vf = ('drawtext=font=Arial:text=' + Q2 + safe + Q2
	 + ':fontsize=' + str(fontsize)
	 + ':fontcolor=white:borderw=5:bordercolor=black'
	 + ':x=(w-text_w)/2:y=' + ypos
	 + ':alpha=' + Q2 + alpha + Q2
	 + ':enable=' + Q2 + 'between(t,0,' + str(duration) + ')' + Q2)
	cmd = [_ff(), '-y', '-i', path, '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', tmp]
	r = subprocess.run(cmd, capture_output=True)
	if r.returncode == 0 and os.path.exists(tmp):
		os.replace(tmp, path)
		return True
	return False