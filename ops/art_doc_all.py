# -- coding: utf-8 --
"""Build + publish ALL 10 art-documentary videos sequentially."""
import os
import sys
import io
import json
import time

sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from ops import art_doc as ad
from projects.art_doc.art_list import ARTS

SECTIONS = 12


def build_one(art):
	slug = art['slug']
	t0 = time.time()
	out_dir = os.path.join(ad.OUTDIR, 'artdoc_' + slug + '.result.json')
	if os.path.exists(out_dir):
		ad.log('SKIP (done):', slug)
		return json.load(open(out_dir, encoding='utf-8'))
	ad.log('===== BUILD', slug, '=====')
	os.makedirs(ad.ASSETS, exist_ok=True)
	img = os.path.join(ad.ASSETS, slug + 'main.jpg')
	if not os.path.exists(img):
		u = ad.search_image(art['title'] + ' painting', 1280)
		ad.fetch_image(u, img)
	final, sc = ad.build_art_video(art['title'], art['facts'], [img], slug, sections=SECTIONS)
	dur = ad._ffprobe_dur(final)
	title = ((sc or {}).get('title') or art['title'])[:95]
	desc = ((sc or {}).get('hook') or art['facts'])[:400] + ' #art #documentary'
	from ops import os_publish
	res = os_publish.publish(final, title, description=desc, tags=['art', 'documentary', art['slug']], privacy='public', topic='artdoc' + slug, category_id='27', force=True)
	result = {'slug': slug, 'video': final, 'dur': dur, 'dur_min': round(dur / 60, 1), 'title': title, 'publish': res, 'time_s': round(time.time() - t0, 1)}
	open(out_dir, 'w', encoding='utf-8').write(json.dumps(result, ensure_ascii=False, indent=2, default=str))
	ad.log('DONE', slug, res)
	return result


def main():
	results = []
	for art in ARTS:
		try:
			r = build_one(art)
			results.append(r)
		except Exception as e:
			import traceback
			ad.log('ERROR', art['slug'], str(e))
			open(os.path.join(ad.OUTDIR, 'artdoc' + art['slug'] + '.error.txt'), 'w', encoding='utf-8').write(traceback.format_exc())
	ad.log('ALL DONE', len(results), '/', len(ARTS))
	return 0


raise SystemExit(main())
