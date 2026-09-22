# ab_hook.py - render variants with different hooks for A/B test
import os, sys, json
sys.path.insert(0, os.getcwd())
from ops import ffmpeg_render as FR
from ops import hook_engine as HE

def variants(item, n=2, seed=0):
 topic = item.get('topic', '')
 base = item.get('hook', '')
 gen = HE.best(topic, n, seed) if topic else []
 hooks = [base] + [h for h in gen if h != base]
 return hooks[:n]

def _variant_item(item, h, i):
 it = dict(item); it['hook'] = h
 it['id'] = str(item.get('id', 'x')) + '_v' + str(i)
 return it

def render_ab(item, outdir, n=2, seed=0):
 os.makedirs(outdir, exist_ok=True)
 hs = variants(item, n, seed)
 items = [_variant_item(item, h, i) for i, h in enumerate(hs)]
 paths = [os.path.join(outdir, it['id'] + '.mp4') for it in items]
 outs = [FR.render(it, pth, seed=seed + i) for i, (it, pth) in enumerate(zip(items, paths))]
 return list(zip(hs, paths, outs))
