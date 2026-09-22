#!/usr/bin/env bash
# git_push_cloud.sh - tao repo RIENG cho media/ va push len GitHub
# Tranh lan repo cha D:/TNT_AI (chua core)
set -e

cd "$(dirname "$0")/.."

echo "[1] Init repo rieng trong media/"
if [ ! -d .git ]; then
 git init
 git branch -M main
fi

echo "[2] Kiem tra secrets KHONG bi push"
git check-ignore memory/token_new_channel.json && echo " OK: token bi chan"
git check-ignore system/state.db && echo " OK: db bi chan"

echo "[3] Add + commit"
git add .
git commit -m "TNT Media OS - cloud deploy ready" || true

echo "[4] Tao repo tren GitHub (thu cong):"
echo " https://github.com/new -> name: tnt-media -> Private -> Create"
echo ""
read -p "Nhap GitHub repo URL (vd https://github.com/user/tnt-media.git): " URL

git remote remove origin 2>/dev/null || true
git remote add origin $URL
git push -u origin main

echo "DONE. Repo da san sang de deploy ClawCloud/Zeabur."
