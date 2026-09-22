import os, sys, subprocess
sys.path.insert(0, os.getcwd())
from ops import voice_master as VM
d = VM.duration('output/pika_vo.mp3')
print('voice duration:', d)