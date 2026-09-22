# -- coding: utf-8 --
"""Build ONE art-documentary video end-to-end and optionally publish.

Usage: python ops/art_doc_run.py <slug> [--sections N] [--publish]
"""
import os
import sys
import io
import json
import time

sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from ops import art_doc as ad
from projects.art_doc.art_list import ARTS


def find_art(slug):
	for a in ARTS:
		if a['slug'] == slug:
			return a
	return None


def fetch_images(art, n=1):
	os.makedirs(ad.ASSETS, exist_ok=True)
	imgs = []
	main = os.path.join(ad.ASSETS, art['slug'] + '_main.jpg')
	if not os.path.exists(main):
		u = ad.search_image(art['title'] + ' painting', 1280)
		ad.fetch_image(u, main)
	imgs.append(main)
	return imgs

def main():
	slug = sys.argv[1] if len(sys.argv) > 1 else None
	sections = 8
	publish = '--publish' in sys.argv
	if '--sections' in sys.argv:
		sections = int(sys.argv[sys.argv.index('--sections') + 1])
	if not slug:
		print('usage: art_doc_run.py <slug>')
		return 2
	art = find_art(slug)
	if not art:
		print('art not found:', slug)
		return 2
	t0 = time.time()
	log = ad.log
	log('=== BUILD', slug, '===')
	imgs = fetch_images(art)
	log('images:', imgs)
	final, sc = ad.build_art_video(art['title'], art['facts'], imgs, slug, sections=sections)
	dur = ad._ffprobe_dur(final)
	log('DONE', final, 'dur_min', round(dur/60, 1), 'time_s', round(time.time()-t0,1))
	result = {'slug': slug, 'video': final, 'dur': dur, 'title': (sc or {}).get('title'), 'time': round(time.time()-t0,1)}
	if publish:
		from ops import os_publish
		title = ((sc or {}).get('title') or art['title'])[:95]
		desc = ((sc or {}).get('hook') or art['facts'])[:400] + ' #art #documentary'
		res = os_publish.publish(final, title, description=desc, tags=['art', 'documentary', art['slug']], privacy='public', topic='artdoc' + slug, category_id='27', force=True)
		result['publish'] = res
		log('PUBLISHED', res)
	open(os.path.join(ad.OUTDIR, 'artdoc' + slug + '.result.json'), 'w', encoding='utf-8').write(json.dumps(result, ensure_ascii=False, indent=2, default=str))
	return 0


raise SystemExit(main())
