import os, sys, io, json, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.abspath('.')
sys.path.insert(0, ROOT)


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('--topic', default=None)
	ap.add_argument('--dry-run', action='store_true')
	ap.add_argument('--privacy', default='public')
	args = ap.parse_args()
	from ops import auto_publish, topic_picker
	topic = args.topic
	if not topic:
		topic = topic_picker.pick()
		print('[PICK] fresh topic =', topic)
	else:
		print('[PICK] forced topic =', topic)
	if not topic:
		print('[STOP] no fresh topic available.')
		return 2
	if args.topic and auto_publish._already_published(topic):
		print('[STOP] already published, refusing:', topic)
		return 3
	print('[BUILD] building NEW video ...')
	res = auto_publish.run(topic=topic, privacy=args.privacy, force=False, allow_republish=False)
	print('[RESULT]')
	print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
	return 0 if res.get('ok') else 1


raise SystemExit(main())
