import os, json, time, random, hashlib, urllib.request, urllib.parse, socket
from pathlib import Path
from ops.trend_cc import get_trends
from ops.script_cc import gen_script
from ops.media_cc import fetch_media
from ops.title_cc import gen_title
from ops.uploader_cc import upload_short
from ops.render_cc import make_text_card, render_slideshow

ROOT = Path(file).resolve().parent.parent
STATE = ROOT / 'memory' / 'state.json'
MEDIA = ROOT / 'media'
MEDIA.mkdir(exist_ok=True)

socket.setdefaulttimeout(8)


def load_state():
 s = {}
 if STATE.exists():
 try:
 s = json.loads(STATE.read_text(encoding='utf-8'))
 except Exception:
 s = {}
 for k in ('posted', 'used_topics', 'used_titles', 'used_angles'):
 if not isinstance(s.get(k), list):
 s[k] = []
 s['version'] = 2
 return s


def save_state(s):
 for k in ('posted', 'used_topics', 'used_titles', 'used_angles'):
 s[k] = s[k][-500:]
 STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')


def try_download(url, out, timeout=6):
 try:
 req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
 with urllib.request.urlopen(req, timeout=timeout) as r, open(out, 'wb') as f:
 f.write(r.read())
 return os.path.getsize(out) > 8000
 except Exception:
 return False


def script_beats(script):
 if isinstance(script, dict):
 parts = [script.get('hook', '')] + list(script.get('body', []) or []) + [script.get('cta', '')]
 return [b for b in parts if b]
 return [str(script)]


def produce_video(script, media, ch, use_remote=False):
 name = ch['name']
 ts = int(time.time())
 out_dir = MEDIA / name
 out_dir.mkdir(exist_ok=True)
 out_path = out_dir / f'{name}{ts}.mp4'

 beats = script_beats(script)
 cards = []
 queries = [m.get('query', '') for m in (media or [])]

 for i, beat in enumerate(beats):
 got = False
 if use_remote and i < len(queries):
 img_path = out_dir / f'{name}{ts}{i}.jpg'
 enc = urllib.parse.quote(queries[i])
 url = 'https://source.unsplash.com/1080x1920/?' + enc
 if try_download(url, img_path):
 cards.append(str(img_path))
 got = True
 if not got:
 card = out_dir / f'{name}{ts}_{i}_card.jpg'
 make_text_card(beat, str(card), tag=ch['name'])
 cards.append(str(card))

 per = max(2.0, min(4.0, 45.0 / max(1, len(cards))))
 render_slideshow(cards, out_path, per_card=per)
 return str(out_path), None


def run_channel(ch, dry=False, use_remote=False):
 state = load_state()
 niche = ch.get('niche', 'general')
 lang = ch.get('language', 'vi')
 seed = hashlib.md5(f"{ch['name']}|{time.time()}|{random.random()}".encode()).hexdigest()[:8]

 trends = get_trends(niche, lang, state['used_topics'], n=6)
 if not trends:
 return {'status': 'error', 'reason': 'no_topics'}
 topic = random.choice(trends)

 script = gen_script(topic, niche, lang, state['used_angles'], seed=seed)
 angle = (script.get('hook', '')[:80] if isinstance(script, dict) else str(script)[:80])
 media = fetch_media(topic, niche, script=script)
 title = gen_title(topic, script, lang, state['used_titles'], niche=niche)

 video_path, err = produce_video(script, media, ch, use_remote=use_remote)
 if err:
 return {'status': 'error', 'reason': err, 'topic': topic}

 if dry:
 result = {'status': 'dry', 'video': video_path, 'title': title, 'topic': topic}
 else:
 result = upload_short(video_path, title, script, ch)

 if result.get('status') in ('ok', 'dry'):
 state['posted'].append({'topic': topic, 'title': title, 'ts': time.time(), 'channel': ch['name']})
 state['used_topics'].append(topic)
 state['used_titles'].append(title)
 if angle:
 state['used_angles'].append(angle)
 save_state(state)
 return result


def main():
 cfg = json.loads((ROOT / 'config' / 'channels.json').read_text(encoding='utf-8'))
 for ch in cfg['channels']:
 print(run_channel(ch))


if name == 'main':
 main()
