# CHECKLIST YC5 - Oracle Cloud (0 dong/thang)

## Buoc 1: Tao tai khoan Oracle Cloud (neu chua co)
[ ] Mo https://signup.cloud.oracle.com/
[ ] Dang ky (can the Visa/Master, se khong bi tru tien o Always Free)
[ ] Chon Home Region: Singapore hoac Japan (gan VN, free tier tot)

## Buoc 2: Tao VM Always-Free
[ ] Vao Compute -> Instances -> Create Instance
[ ] Name: tnt-media
[ ] Image: Ubuntu 22.04 (aarch64/ARM)
[ ] Shape: VM.Standard.A1.Flex -> 4 OCPU / 24 GB RAM (Always Free)
[ ] Boot volume: 100 GB
[ ] Add SSH key: upload public key cua ban (hoac tao moi)
[ ] Create -> doi ~1 phut -> copy Public IP

## Buoc 3: Mo port (Security List)
[ ] VCN -> Security Lists -> Default -> Add Ingress Rule
[ ] Source 0.0.0.0/0, TCP port 8787 (dashboard)

## Buoc 4: Day code len VM (chay tren may Windows nay)
[ ] Mo Git Bash / WSL / PowerShell co ssh
[ ] cd D:/TNT_AI/venture_foundry/media
[ ] bash deploy/push_to_vm.sh <VM_IP> ubuntu

## Buoc 5: Copy file bi mat len VM
[ ] scp .env ubuntu@<VM_IP>:/opt/tnt/media/.env
[ ] scp memory/token_new_channel.json ubuntu@<VM_IP>:/opt/tnt/media/memory/
[ ] scp config/token.pickle ubuntu@<VM_IP>:/opt/tnt/media/config/
[ ] scp memory/tnt_media.db ubuntu@<VM_IP>:/opt/tnt/media/memory/
[ ] scp system/state.db ubuntu@<VM_IP>:/opt/tnt/media/system/

## Buoc 6: Khoi dong
[ ] ssh ubuntu@<VM_IP>
[ ] sudo systemctl start tnt-scheduler tnt-dashboard
[ ] sudo systemctl status tnt-scheduler

## Buoc 7: Kiem tra
[ ] http://<VM_IP>:8787 -> dashboard
[ ] http://<VM_IP>:8787/api/quotas -> quota 2 kenh
[ ] tail -f /opt/tnt/media/logs/scheduler_cc.log

## Ket qua mong doi
- Scheduler tu dong chay Mialinhcute 9/15/21h, vilevi5676 8/12/18/21h (gio VM)
- Moi lan chay: build 1 clip moi + publish + ghi ledger
- Dashboard xem quota/kenh/token
