#!/usr/bin/env bash
set -e

# start.sh - chay scheduler + dashboard trong 1 container (cloud deploy)
cd /app

echo "[start] TNT Media OS booting..."

# Seed media tu cloud_media neu library rong
if [ -d /app/cloud_media/library ] && [ -z "$(ls -A /app/library 2>/dev/null)" ]; then
	echo "[start] seeding library from cloud_media..."
	mkdir -p /app/library /app/music_bank
	cp -rn /app/cloud_media/library/. /app/library/ 2>/dev/null || true
	cp -rn /app/cloud_media/music_bank/. /app/music_bank/ 2>/dev/null || true
fi

echo "[start] channel cron:"
python -c "import sqlite3;c=sqlite3.connect('system/state.db');[print(' ',r[0],r[1]) for r in c.execute('SELECT name,scheduleCron FROM channels WHERE active=1')]" || true

# Scheduler o background
python ops/scheduler_cc.py &
echo "[start] scheduler started"

# Dashboard giu container song
echo "[start] dashboard on :8787"
exec python _serve.py
