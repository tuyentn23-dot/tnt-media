# YC5 - Deploy Oracle Cloud Always-Free (0d/thang)

## 1. Tao VM
- Oracle Cloud -> Compute -> Instances -> Create
- Shape: VM.Standard.A1.Flex (ARM Ampere) - Always Free: 4 OCPU / 24GB RAM
- Image: Ubuntu 22.04 (aarch64)
- Add SSH key, mo port 22 va 8787 (dashboard) trong Security List

## 2. Copy code len VM

scp -r media ubuntu@<VM_IP>:/tmp/media
ssh ubuntu@<VM_IP> "sudo mkdir -p /opt/tnt && sudo mv /tmp/media /opt/tnt/media"


## 3. Chay bootstrap

ssh ubuntu@<VM_IP>
sudo bash /opt/tnt/media/deploy/oracle_setup.sh


## 4. Khoi dong

sudo systemctl start tnt-scheduler tnt-dashboard
sudo systemctl status tnt-scheduler


## 5. Upload token YouTube
- Copy memory/token_new_channel.json + config/token.pickle len VM cung duong dan
- Copy .env (GROQ_API_KEY...) len VM

## 6. Kiem tra
- Dashboard: http://<VM_IP>:8787
- Quota API: http://<VM_IP>:8787/api/quotas
- Log: /opt/tnt/media/logs/scheduler_cc.log

## Ghi chu
- ARM aarch64: ffmpeg co san trong apt, Pillow/pydub cai qua pip binh thuong
- Neu dung Docker: docker compose -f deploy/docker-compose.yml up -d
- Scheduler doc cron tu bang channels (Mialinhcute 9/15/21, vilevi5676 8/12/18/21)
