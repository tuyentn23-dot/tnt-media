# -- coding: utf-8 --
# pipeline/state.py - SQLite state API (NGUON SU THAT DUY NHAT)
import os, sys, json, sqlite3, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'state', 'pipeline.db')

SCHEMA = '''
CREATE TABLE IF NOT EXISTS channels (
	id TEXT PRIMARY KEY,
	enabled INTEGER DEFAULT 1,
	niche TEXT, forbidden TEXT, kinds TEXT,
	voice TEXT, max_length_sec INTEGER DEFAULT 60,
	style TEXT, schedule TEXT,
	publish_mode TEXT DEFAULT 'approve',
	quality_gate TEXT DEFAULT 'normal',
	created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS jobs (
	id TEXT PRIMARY KEY,
	channel_id TEXT NOT NULL,
	topic TEXT, kind TEXT,
	length_override INTEGER, voice_override TEXT, voice_preset TEXT, music_mood TEXT,
	count INTEGER DEFAULT 1, require_approval INTEGER DEFAULT 1,
	run_at TEXT, repeat TEXT,
	status TEXT DEFAULT 'pending', priority INTEGER DEFAULT 5,
	created_by TEXT, created_at TEXT, updated_at TEXT, error TEXT
);
CREATE TABLE IF NOT EXISTS publications (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	job_id TEXT, channel_id TEXT, signature TEXT UNIQUE,
	topic TEXT, kind TEXT, title TEXT, youtube_id TEXT, file_path TEXT,
	status TEXT, view_count INTEGER DEFAULT 0, like_count INTEGER DEFAULT 0,
	quota_cost INTEGER DEFAULT 0, published_at TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS topics (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	channel_id TEXT, kind TEXT, topic TEXT, source TEXT,
	score REAL DEFAULT 0, last_used TEXT, cooldown_until TEXT,
	created_at TEXT, UNIQUE(channel_id, kind, topic)
);
CREATE TABLE IF NOT EXISTS assets (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	kind TEXT, path TEXT UNIQUE, meta TEXT, enabled INTEGER DEFAULT 1, created_at TEXT
);
CREATE TABLE IF NOT EXISTS audit (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	session TEXT, actor TEXT, action TEXT, target TEXT, version_from TEXT, version_to TEXT, reason TEXT, ts TEXT
);
CREATE TABLE IF NOT EXISTS quota (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	account TEXT, date TEXT, units_used INTEGER DEFAULT 0, units_total INTEGER DEFAULT 10000, UNIQUE(account, date)
);
CREATE TABLE IF NOT EXISTS modules_ver (
	name TEXT, version TEXT, installed_at TEXT, meta TEXT, PRIMARY KEY(name, version)
);
CREATE TABLE IF NOT EXISTS trends (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	topic TEXT, kind TEXT, source TEXT, score REAL, velocity REAL, ts TEXT
);
CREATE INDEX IF NOT EXISTS idx_pub_chan ON publications(channel_id);
CREATE INDEX IF NOT EXISTS idx_pub_sig ON publications(signature);
CREATE INDEX IF NOT EXISTS idx_job_status ON jobs(status);
'''


def connect():
	os.makedirs(os.path.dirname(DB), exist_ok=True)
	c = sqlite3.connect(DB, timeout=30)
	c.row_factory = sqlite3.Row
	c.execute('PRAGMA journal_mode=WAL')
	return c


def init():
	c = connect()
	c.executescript(SCHEMA)
	try:
		c.execute('ALTER TABLE jobs ADD COLUMN voice_preset TEXT')
	except Exception:
		pass
	c.commit()
	return c


def now():
	return time.strftime('%Y-%m-%dT%H:%M:%S')


if __name__ == '__main__':
	c = init()
	print('[state] DB ready: ', DB)
	rows = c.execute('SELECT name FROM sqlite_master').fetchall()
	print('[state] tables: ', [r[0] for r in rows])
