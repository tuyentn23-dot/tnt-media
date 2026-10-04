# -- coding: utf-8 --
# Pipeline san xuat video hoan chinh: script -> build -> voice -> caps -> hook -> QC
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ops import vids_edit as ve
from ops import vids_post as vp
from ops import effects as ef
from ops import quality_check as qc
from ops import script_templates as st

def make(folder, topic, out_path, theme='pink', aspect='9:16', n=6, seg=2.0, music=None, cta=True):
	"""San xuat 1 video Shorts hoan chinh."""
	if not music:
		music = 'assets/music_clips/clip_0_0.mp3'
	
	# 1. Script
	voice, hook, caps = st.to_segments(topic)
	print('[1] Script: hook=' + hook[:40], flush=True)
	
	# 2. Build base video
	os.makedirs(os.path.dirname(out_path), exist_ok=True)
	r = ve.build(folder, out_path, voice_text=None, hook=None, caps=None, theme=theme, n=n, seg=seg, music=music, aspect=aspect)
	if not r.get('ok'):
		return {'ok': False, 'err': 'build: ' + str(r.get('err', '?'))}
	dur0 = ve._dur(out_path)
	print('[2] Build: ' + str(round(dur0, 2)) + 's', flush=True)
	
	# 3. Voice
	vp.add_voice(out_path, voice)
	dur1 = ve._dur(out_path)
	print('[3] Voice: ' + str(round(dur1, 2)) + 's', flush=True)
	
	# 4. Captions
	all_caps = [hook] + list(caps) + (['Theo dõi để xem thêm!'] if cta else [])
	segs = []
	i = 2.5 # hook da hien qua hook_text
	per = (dur1 - i) / max(1, len(caps))
	for c in caps:
		segs.append((i, i + per, c))
		i += per
	vp.add_captions(out_path, segs, theme=theme)
	print('[4] Captions: ' + str(len(segs)), flush=True)
	
	# 5. Hook text animation
	ef.hook_text(out_path, hook, duration=2.5, fontsize=72)
	print('[5] Hook text OK', flush=True)
	
	# 6. Quality gate
	q = qc.evaluate(out_path, hook)
	print('[6] QC: ' + str(q['ok']) + ' ' + str(q['errors']), flush=True)
	
	return {'ok': q['ok'], 'path': out_path, 'dur': ve._dur(out_path), 'qc': q, 'hook': hook, 'voice_text': voice, 'captions': caps, 'folder': folder, 'topic': topic}
