import os, json, time
from pathlib import Path
from flask import Flask, jsonify, request

ROOT = Path(file).resolve().parent
STATE = ROOT / 'memory' / 'state.json'
CONFIG = ROOT / 'config' / 'channels.json'
LOG = ROOT / 'memory' / 'logs' / 'upload.log'

app = Flask(name)


def _load_state():
 if STATE.exists():
 try:
 return json.loads(STATE.read_text(encoding='utf-8'))
 except Exception:
 return {}
 return {}


def _load_channels():
 if CONFIG.exists():
 try:
 return json.loads(CONFIG.read_text(encoding='utf-8')).get('channels', [])
 except Exception:
 return []
 return []


@app.route('/')
def index():
 chans = _load_channels()
 return '<h1>TNT Media OS</h1><p>OK. Channels: ' + ', '.join(c['name'] for c in chans) + '</p>'


@app.route('/api/status')
def api_status():
 return jsonify({'ok': True, 'ts': time.time(), 'service': 'tnt-media-os'})


@app.route('/api/os/state')
def api_state():
 s = _load_state()
 return jsonify({
 'version': s.get('version', 1),
 'posted_count': len(s.get('posted', [])),
 'used_topics_count': len(s.get('used_topics', [])),
 'used_titles_count': len(s.get('used_titles', [])),
 'last_posted': s.get('posted', [])[-5:],
 })


@app.route('/api/quotas')
def api_quotas():
 # YouTube Data API quota: 10,000 units/day; upload = 1600 units
 s = _load_state()
 today = time.strftime('%Y-%m-%d')
 posted_today = [p for p in s.get('posted', []) if time.strftime('%Y-%m-%d', time.localtime(p.get('ts', 0))) == today]
 used = len(posted_today) * 1600
 return jsonify({
 'daily_quota': 10000,
 'used_today': used,
 'remaining': max(0, 10000 - used),
 'uploads_today': len(posted_today),
 })


@app.route('/api/run', methods=['POST'])
def api_run():
 from ops.pipeline_cc import run_channel
 name = request.json.get('channel') if request.is_json else None
 chans = _load_channels()
 results = []
 for ch in chans:
 if name and ch['name'] != name:
 continue
 try:
 results.append({'channel': ch['name'], 'result': run_channel(ch)})
 except Exception as e:
 results.append({'channel': ch['name'], 'error': repr(e)})
 return jsonify({'results': results})


if name == 'main':
 app.run(host='0.0.0.0', port=7860)
