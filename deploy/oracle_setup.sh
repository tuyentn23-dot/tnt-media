#!/usr/bin/env bash
set -euo pipefail

# YC5 - Oracle Cloud Always-Free VM bootstrap for TNT Media OS
# Usage: sudo bash deploy/oracle_setup.sh

APP_DIR=/opt/tnt/media
APP_USER=tnt

echo "[1/6] apt deps"
apt-get update -y
apt-get install -y python3 python3-pip python3-venv ffmpeg git curl

echo "[2/6] user"
id -u $APP_USER >/dev/null 2>&1 || useradd -m -s /bin/bash $APP_USER

echo "[3/6] app dir"
mkdir -p $APP_DIR
chown -R $APP_USER:$APP_USER $APP_DIR

echo "[4/6] venv + deps"
sudo -u $APP_USER python3 -m venv $APP_DIR/.venv || true
sudo -u $APP_USER $APP_DIR/.venv/bin/pip install --upgrade pip || true
if [ -f $APP_DIR/requirements.txt ]; then sudo -u $APP_USER $APP_DIR/.venv/bin/pip install -r $APP_DIR/requirements.txt; fi

echo "[5/6] systemd units"
cp $APP_DIR/deploy/tnt-scheduler.service /etc/systemd/system/
cp $APP_DIR/deploy/tnt-dashboard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable tnt-scheduler.service tnt-dashboard.service

echo "[6/6] firewall (optional)"
iptables -I INPUT -p tcp --dport 8787 -j ACCEPT || true

echo "DONE. Start: systemctl start tnt-scheduler tnt-dashboard"
