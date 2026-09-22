# -*- coding: utf-8 -*-
# ops/mia_content.py - Quan ly noi dung kenh Mia
import os, sys, json, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
MIADB = os.path.join(ROOT, "channels", "Mialinhcute", "content_db.json")
LEDGER = os.path.join(ROOT, "channels", "Mialinhcute", "published_ledger.json")
POOL = os.path.join(ROOT, "channels", "Mialinhcute", "topic_pool.json")

NEW_TOPIC_SOURCES = {
	"anime": ["pokemon", "naruto", "onepiece", "dragonball", "sailormoon"],
	"roblox": ["adoptme", "bloxfruits", "brookhaven", "mm2", "piggy"],
	"cute_animals": ["shiba", "panda", "axolotl", "quokka", "fennec"],
	"meme": ["funny_cat_fail", "funny_dog", "satisfying_slime", "oddly_satisfying", "funny_animals"],
}

PEXELS_QUERY = {
	"pokemon": "anime cartoon", "naruto": "japanese anime", "onepiece": "anime sea",
	"dragonball": "anime action", "sailormoon": "anime girl",
	"adoptme": "cute pets game", "bloxfruits": "gaming adventure",
	"brookhaven": "city roleplay game", "mm2": "mystery game", "piggy": "horror game",
	"shiba": "shiba inu dog", "panda": "panda bear", "axolotl": "axolotl",
	"quokka": "quokka animal", "fennec": "fennec fox",
	"funny_cat_fail": "funny cat fail", "funny_dog": "funny dog",
	"satisfying_slime": "satisfying slime", "oddly_satisfying": "oddly satisfying",
	"funny_animals": "funny animals",
}

def _load(path, default):
	if os.path.exists(path):
		try:
			return json.load(io.open(path, encoding="utf-8"))
		except Exception:
			return default
	return default

def _save(path, data):
	io.open(path, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))

def published_ids():
	led = _load(LEDGER, {"signatures": {}})
	return set(led.get("signatures", {}).keys())

def is_used(item_id, kind):
	sig = kind + "|" + item_id + "|"
	return any(s.startswith(sig) for s in published_ids())

def fresh_items(kind):
	db = _load(MIADB, {})
	return [it for it in db.get(kind, []) if not is_used(it.get("id", ""), kind)]

def next_topic(kind):
	pool = _load(POOL, {})
	used_kind = set(pool.get("used", {}).get(kind, []))
	fresh = [t for t in NEW_TOPIC_SOURCES.get(kind, []) if t not in used_kind]
	return fresh[0] if fresh else None

def mark_topic(kind, topic):
	pool = _load(POOL, {})
	lst = pool.setdefault("used", {}).setdefault(kind, [])
	if topic not in lst:
		lst.append(topic)
	_save(POOL, pool)

def fetch_footage(kind, topic, take=3):
	from ops import pexels_fetcher as pf
	base = os.path.join(ROOT, "library", kind)
	os.makedirs(base, exist_ok=True)
	q = PEXELS_QUERY.get(topic, topic.replace("_", " "))
	us = pf.urls(q, per=6)
	saved = []
	for i, u in enumerate(us[:take]):
		fn = os.path.join(base, "px_" + topic + "_" + str(i) + ".mp4")
		if os.path.exists(fn):
			saved.append(fn)
			continue
		try:
			pf.download(u, fn)
			saved.append(fn)
		except Exception:
			pass
	return saved