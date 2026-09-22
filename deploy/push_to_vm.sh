#!/usr/bin/env bash
# YC5 - push TNT Media code to Oracle VM
set -euo pipefail

VM_IP=${1:?Usage: push_to_vm.sh <VM_IP> [user]}
USER=${2:-ubuntu}

echo "Packaging..."
tar --exclude=.venv --exclude=__pycache__ --exclude=.git --exclude=output --exclude=_trash --exclude=backups -czf /tmp/tnt_media.tgz .

echo "Uploading to $USER@$VM_IP..."
scp /tmp/tnt_media.tgz $USER@$VM_IP:/tmp/

echo "Extracting on VM..."
ssh $USER@$VM_IP "sudo mkdir -p /opt/tnt/media && sudo tar -xzf /tmp/tnt_media.tgz -C /opt/tnt/media"

echo "Running bootstrap..."
ssh $USER@$VM_IP "sudo bash /opt/tnt/media/deploy/oracle_setup.sh"

echo "DONE. Copy .env + tokens, then start services."
