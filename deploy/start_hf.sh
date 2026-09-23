#!/usr/bin/env bash
set -e
cd /app

echo "[hf] TNT Media OS booting on :7860"

if [ ! -d /app/cloud_media/library ]; then
	if [ -n "$GITHUB_TOKEN" ]; then
		echo "[hf] downloading cloud_media from GitHub..."
		REPO="tuyentn23-dot/tnt-media"
		BR="main"
		mkdir -p /tmp/cm && cd /tmp/cm
		curl -sL -H "Authorization: token $GITHUB_TOKEN" \
			https://api.github.com/repos/$REPO/tarball/$BR -o repo.tgz
		tar -xzf repo.tgz --strip-components=1
		cp -rn cloud_media /app/ 2>/dev/null || true
		cd /app
	fi
fi

if [ -d /app/cloud_media/library ] && [ -z "$(ls -A /app/library 2>/dev/null)" ]; then
	echo "[hf] seeding library..."
	mkdir -p /app/library /app/music_bank
	cp -rn /app/cloud_media/library/. /app/library/ 2>/dev/null || true
	cp -rn /app/cloud_media/music_bank/. /app/music_bank/ 2>/dev/null || true
fi

export IMAGEIO_FFMPEG_EXE=$(which ffmpeg || echo /usr/bin/ffmpeg)

python ops/scheduler_cc.py &
echo "[hf] scheduler started"

export PORT=7860
export HOST=0.0.0.0
exec python _serve.py
