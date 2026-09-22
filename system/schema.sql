-- TNT Media OS — SQLite Schema v1
-- All lines start at column 0 to survive wrapper indentation stripping.
-- Column names use camelCase (no underscores) for same reason.

PRAGMA journalMode = WAL;
PRAGMA foreignKeys = ON;

CREATE TABLE IF NOT EXISTS channels (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE NOT NULL,
platform TEXT NOT NULL DEFAULT 'youtube',
tokenPath TEXT,
active INTEGER NOT NULL DEFAULT 1,
scheduleCron TEXT,
aspect TEXT DEFAULT '9:16',
maxSeconds INTEGER DEFAULT 60,
voicePreset TEXT,
styleJson TEXT,
rulesJson TEXT,
weightsJson TEXT,
trendSourcesJson TEXT,
createdAt TEXT NOT NULL DEFAULT (datetime('now')),
updatedAt TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tools (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE NOT NULL,
path TEXT NOT NULL,
version TEXT,
argsSchemaJson TEXT,
description TEXT,
lastRunAt TEXT,
health TEXT DEFAULT 'unknown',
createdAt TEXT NOT NULL DEFAULT (datetime('now')),
updatedAt TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS rules (
id INTEGER PRIMARY KEY AUTOINCREMENT,
channelId INTEGER,
ruleType TEXT NOT NULL,
expression TEXT NOT NULL,
severity TEXT DEFAULT 'block',
description TEXT,
active INTEGER NOT NULL DEFAULT 1,
createdAt TEXT NOT NULL DEFAULT (datetime('now')),
FOREIGN KEY (channelId) REFERENCES channels(id)
);

CREATE TABLE IF NOT EXISTS trends (
id INTEGER PRIMARY KEY AUTOINCREMENT,
source TEXT NOT NULL,
region TEXT,
topic TEXT NOT NULL,
score REAL,
volume INTEGER,
growth REAL,
snapshotAt TEXT NOT NULL,
metaJson TEXT
);
CREATE INDEX IF NOT EXISTS idxTrendsTopic ON trends(topic);
CREATE INDEX IF NOT EXISTS idxTrendsSnapshot ON trends(snapshotAt);

CREATE TABLE IF NOT EXISTS decisions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
channelId INTEGER NOT NULL,
trendId INTEGER,
topic TEXT NOT NULL,
format TEXT,
hook TEXT,
score REAL,
weightsSnapshotJson TEXT,
rationale TEXT,
chosenAt TEXT NOT NULL DEFAULT (datetime('now')),
FOREIGN KEY (channelId) REFERENCES channels(id),
FOREIGN KEY (trendId) REFERENCES trends(id)
);

CREATE TABLE IF NOT EXISTS videos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
channelId INTEGER NOT NULL,
decisionId INTEGER,
path TEXT NOT NULL,
status TEXT NOT NULL DEFAULT 'queued',
renderWorker TEXT,
renderMs INTEGER,
metaJson TEXT,
createdAt TEXT NOT NULL DEFAULT (datetime('now')),
FOREIGN KEY (channelId) REFERENCES channels(id),
FOREIGN KEY (decisionId) REFERENCES decisions(id)
);
CREATE INDEX IF NOT EXISTS idxVideosStatus ON videos(status);

CREATE TABLE IF NOT EXISTS publishes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
videoId INTEGER NOT NULL,
platform TEXT NOT NULL,
url TEXT,
publishedAt TEXT,
status TEXT DEFAULT 'pending',
errorText TEXT,
metaJson TEXT,
FOREIGN KEY (videoId) REFERENCES videos(id)
);
CREATE INDEX IF NOT EXISTS idxPublishesAt ON publishes(publishedAt);

CREATE TABLE IF NOT EXISTS analytics (
id INTEGER PRIMARY KEY AUTOINCREMENT,
videoId INTEGER NOT NULL,
views INTEGER DEFAULT 0,
likes INTEGER DEFAULT 0,
comments INTEGER DEFAULT 0,
retention REAL,
ctr REAL,
fetchedAt TEXT NOT NULL,
FOREIGN KEY (videoId) REFERENCES videos(id)
);
CREATE INDEX IF NOT EXISTS idxAnalyticsVideo ON analytics(videoId);

CREATE TABLE IF NOT EXISTS prompts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
version INTEGER NOT NULL,
content TEXT NOT NULL,
abGroup TEXT,
winRate REAL,
samples INTEGER DEFAULT 0,
active INTEGER NOT NULL DEFAULT 1,
createdAt TEXT NOT NULL DEFAULT (datetime('now')),
UNIQUE(name, version)
);

CREATE TABLE IF NOT EXISTS experiments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
variantsJson TEXT,
metric TEXT,
winner TEXT,
samples INTEGER DEFAULT 0,
endedAt TEXT,
createdAt TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS versions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
entityType TEXT NOT NULL,
entityId TEXT,
diffJson TEXT,
note TEXT,
createdAt TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS changelog (
id INTEGER PRIMARY KEY AUTOINCREMENT,
version TEXT,
entity TEXT NOT NULL,
change TEXT NOT NULL,
actor TEXT,
createdAt TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS jobs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
channelId INTEGER,
kind TEXT NOT NULL,
payloadJson TEXT,
status TEXT NOT NULL DEFAULT 'queued',
priority INTEGER DEFAULT 5,
attempts INTEGER DEFAULT 0,
lastError TEXT,
scheduledFor TEXT,
startedAt TEXT,
finishedAt TEXT,
createdAt TEXT NOT NULL DEFAULT (datetime('now')),
FOREIGN KEY (channelId) REFERENCES channels(id)
);
CREATE INDEX IF NOT EXISTS idxJobsStatus ON jobs(status, scheduledFor);
