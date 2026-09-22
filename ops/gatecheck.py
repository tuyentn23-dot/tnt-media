import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ops.viral_engine import analyze
p=sys.argv[1] if len(sys.argv)>1 else "output/story_shark_teeth.mp4"
print(analyze(p))
