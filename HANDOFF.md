# HANDOFF - Phien 2026-10-03

## TONG QUAN
Phien nay: don dep git + xay he thong bao ve + nang cap module video.

## 1. TRANG THAI HIEN TAI

- Git working tree = HEAD (sach, day du)
- Server: http://127.0.0.1:7777 OK (142 publications)
- Branch main, ahead origin 73 commits (CHUA PUSH)
- Untracked: chi state/ (browser_profile, pipeline.db - dung, khong commit)

## 2. DA LAM TRONG PHIEN

### Guardian - he thong bao ve (MOI)
- guardian/snapshot.py: snapshot/verify/restore file quan trong
- guardian/safe_fs.py: xoa an toan (archive thay vi xoa)
- guardian/guard.py: wrapper before/verify
- guardian/critical.json: 21 file quan trong
- guardian/README.md: huong dan
- AGENT_RULES.md: quy tac cho AI
- .git/hooks/pre-commit: tu verify truoc commit

### Module video
- ops/vids_edit.py: dung video cat ghep + 9 transition + zoom + add_music
- ops/vids_post.py: caption mau theme + voice tieng Viet
- ops/vids_agent.py: tao video AI (Google Vids)
- launch_chrome.py: mo Chrome CDP

### Fix
- ops/compat.py: moviepy 2.x shim (set_X=with_X, resize/crop)
- ops/autopublish_runner.py: dung topic that thay footage
- ops/os_publish.py: khoi phuc set_channel
- ops/topic_picker.py: khoi phuc trend_scores

## 3. GIT COMMITS PHIEN NAY

08ff90e feat(vids_edit): 9 transition types + add_music
e7caec5 fix(guardian): sua _arch bi pha
9f1dcc9 feat(guardian): he thong bao ve
8d7783e chore(git): bo sung gitignore
9bb728c chore(data): cap nhat channels config memory
9be38db feat(vids): module dung video
6e1f205 fix(vids): dirname rong trong add_voice
195f294 feat(vids): caption nho khong nen den + voiceover

## 4. VAN DE CHUA GIAI QUYET

### Bug duration video (uu tien cao)
- Video build ra chi 5.1s thay vi ~10s (6 segment x 2s)
- Da bo -shortest nhung chua fix duoc
- Can debug _seg + _xfade_join offset

### Quota Google Vids
- Free tier chi 6-10 video/thang, da dung het
- vids_agent tao video AI se fail cho den khi quota hoi
- vids_edit (dung footage tinh) van chay duoc

### 91 file untracked .md
- Nhieu tai lieu (GROWTH_STRATEGY, MILLION_VIEW...)
- Chua review, can quyet dinh giu/xoa

## 5. STASH (backup an toan)

- stash@{0}: backup_modified_20261003 (working tree cu)
- stash@{1}: backup_before_cleanup_20261002
- Co the xoa neu khong can: git stash drop

## 6. LUU Y TOOL

- write_file/run_python hay PHA code: nuot ky tu dac biet
- Cach chong: dung base64 hoac build bang chr()
- cwd hay doi ve D:/TNT_AI -> luon cd ve workspace
- Khong kill python (se tu kill tool)
- Truoc khi xoa file: dung guardian/safe_fs.py remove

## 7. BUOC TIEP THEO

1. Push len remote: git push
2. Fix bug duration video (5.1s -> 10s)
3. Test dung 1 video day du roi dang thu
4. Review 91 file untracked .md
5. Khi quota Vids hoi: tao video AI moi

## 8. LENH NHANH

python guardian/guard.py before # snapshot truoc khi lam
python guardian/guard.py verify # kiem tra sau khi lam
python guardian/safe_fs.py remove X # xoa an toan
python guardian/snapshot.py restore # khoi phuc neu mat file

