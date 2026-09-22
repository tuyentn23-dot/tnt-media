import sys
fn = sys.argv[1]
raw = open(fn, 'rb').read()
fixes = [
	(b"os.path.abspath(file)