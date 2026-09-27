# AGENT RULES — Hiến pháp làm việc của TNT Media OS

Áp dụng cho MỌI phiên agent. Đọc trước khi làm bất cứ gì.

## 5 QUY TẮC BẤT DI BẤT DỊCH

### QT1 — Mục tiêu trước, giải pháp sau
Trước khi viết gì, tự hỏi: "User muốn KẾT QUẢ gì?" (không phải CÁCH gì).
Kết quả là cái bất biến. Cách là cái thay được.

### QT2 — Chọn cách đơn giản nhất chạy được
Thứ tự ưu tiên (chọn bậc THẤP NHẤT đủ dùng):
1. File tĩnh (JSON/MD) — đọc được là xong
2. Script 1 lần (python x.py) — cần logic
3. Script chạy nền — chỉ khi bắt buộc
4. Server / daemon — chỉ khi 3 cái trên không đủ
5. Cloud — chỉ khi máy tắt vẫn cần chạy

Không được nhảy bậc. Bậc 2 đủ thì KHÔNG dùng bậc 4.

### QT3 — Fail 2 lần thì ĐỔI CÁCH
Cùng 1 cách fail 2 lần:
- KHÔNG sửa tiếp cách đó
- DỪNG, phân tích vì sao fail
- Chọn cách khác ở bậc thấp hơn (QT2)

### QT4 — Tôn trọng giới hạn kênh
Wrapper này có giới hạn VẬT LÝ (xem WRAPPER_RULES.md).
Khi chọn cách, hỏi: "Cách này có vượt giới hạn không?"
Nếu có → chọn cách khác. KHÔNG cố lách.

### QT5 — Fail 3 lần thì BÁO USER
Sau 3 lần thử fail:
- DỪNG
- Nói thẳng: "Cách X không khả thi. Đề xuất cách Y."
- Để user quyết
Không tự đâm tiếp.

## CHECKLIST TRƯỚC MỌI VIỆC LỚN

1. Kết quả user muốn là gì? (1 câu)
2. Cách đơn giản nhất đạt kết quả đó? (bậc thấp nhất — QT2)
3. Cách đó có vượt giới hạn kênh không? (QT4)
4. Nếu fail 2 lần, tôi đổi sang cách nào? (QT3)
5. Khi nào tôi báo user? (sau 3 lần — QT5)

## NGUYÊN TẮC BỔ SUNG

- Kết quả > Cách. Kết quả > Code đẹp. Kết quả > Sự hoàn hảo.
- Cái gì chạy được và đơn giản > cái gì đẹp và phức tạp.
- Ghi mọi quyết định vào file để phiên sau đọc. Trí nhớ agent KHÔNG tồn tại giữa các phiên.
- Nếu không chắc, chọn cách đơn giản hơn và hỏi user.
- Không bao giờ sửa file ngoài workspace media/ mà không hỏi.

---

## PHAN II - KY LUAT PIPELINE (Phase 0, 2026-09-23)

### QT6 - Doc STATE truoc khi lam bat cu gi

Thu tu doc BAT BUOC moi phien:
1. STATE.md (tom tat, auto-generated tu DB)
2. PIPELINE_SPEC.md (kien truc + schema)
3. AGENT_RULES.md (file nay)
4. Query state/pipeline.db neu can chi tiet

KHONG doc 4 ledger rai rac nua. Chung se bi xoa o Phase 1.

### QT7 - Chi sua trong modules/

| Duong dan | Duoc sua? |
|---|---|
| modules/* | CO |
| pipeline/* | KHONG (HARD)
| app/* | Chi khi user yeu cau |
| config/*.yaml schema | KHONG |
| state/pipeline.db schema | KHONG |
| PIPELINE_SPEC.md | Chi khi bump version |

### QT8 - Khong tu dang video

Agent KHONG BAO GIO goi truc tiep os_publish, multichannel_runner,
hay bat ky ham publish nao. Moi viec dang phai qua:

bash
python -m pipeline.runner --job-json {...}


Agent DUOC tao job (status=pending), KHONG duoc approve/dang.

### QT9 - Bump version khi sua module

Moi module co MODULE = {"version": "x.y.z"}. Khi sua:
- Bug fix: bump patch (2.0.0 -> 2.0.1)
- Tinh nang moi: bump minor (2.0.0 -> 2.1.0)
- Doi interface: bump major (2.0.0 -> 3.0.0) + bao user

Ghi vao CHANGELOG.md: ngay, module, version, mo ta, ly do.

### QT10 - Selfcheck truoc khi ket thuc phien

bash
python -m pipeline.selfcheck


PASS moi duoc ket thuc. FAIL thi phai sua hoac bao user.

### QT11 - Audit moi thay doi

Truoc khi sua file trong modules/, ghi 1 dong vao audit table:
- Phien nao, ngay nao, file nao, version cu -> moi, ly do

Khong co audit -> khong the rollback -> khong the debug.

---

## PHAN III - MOI TRUONG LAM VIEC (Quan trong!)

### PIII.1 - Bug mang content cua agent tool

Trong phien 2026-09-23, tool bi loi: khi ghi file qua write_file
hoac run_python, moi ky tu Markdown bi strip:
- * (star) -> bi xoa
- _ (underscore) -> bi xoa
- ` (backtick) -> bi xoa
- 4 spaces indent -> 1 space

### PIII.2 - Workaround bat buoc

Dung run_python voi escape:

python
STAR = chr(42) # *
UND = chr(95) # _
BTK = chr(96) # `
TAB = chr(9)
NL = chr(10)

lines = ["def f():", TAB + "return 1"]
open("x.py", "w").write(NL.join(lines) + NL)


### PIII.3 - Verify bat buoc

Sau khi ghi file .py:

bash
python -c "import ast; ast.parse(open('x.py',encoding='utf-8').read()); print('PARSE OK')"


Khong PARSE OK = chua xong.

---

## PHAN IV - CHECKLIST MOI PHIEN

1. [ ] Doc STATE.md + PIPELINE_SPEC.md + file nay
2. [ ] Xac dinh muc tieu (QT1)
3. [ ] Chon cach don gian nhat (QT2)
4. [ ] Sua chi trong modules/ (QT7)
5. [ ] Bump version + ghi CHANGELOG (QT9)
6. [ ] Ghi audit (QT11)
7. [ ] Chay selfcheck (QT10)
8. [ ] Cap nhat STATE.md (auto-generated)
9. [ ] Viet PHIEN_HANDOFF.md cho phien sau

---

## PHAN V - LICH SU

| Ngay | Phien | Thay doi |
|---|---|---|
| 2026-09-23 | Phase 0 | Them PHAN II-V (Pipeline discipline + Moi truong) |


---

# PHẦN 2 — PIPELINE RULES (bat buoc tu Phase 0)

> Ap dung cho moi phien lam viec voi he thong TNT Media moi.
> Chi tiet kien truc: xem PIPELINE_SPEC.md

## 6 NGUYEN TAC BAT DI BAT DICH MOI

### NT1 — Doc STATE truoc, khong doc ledger rai rac
Dau phien, doc theo thu tu:
1. STATE.md (tom tat, auto-generated tu DB)
2. PIPELINE_SPEC.md (kien truc)
3. Query state/pipeline.db neu can chi tiet

CAM doc truc tiep: channels/*/published_ledger.json,
memory/published*.json — day la file cu, se bi xoa o Phase 6.

### NT2 — Chi sua trong modules/
Duoc phep sua:
- modules/**/*.py
- modules/**/*.json (config noi bo module)

CAM sua (tru khi user yeu cau ro):
- pipeline/** — HARD, sua la hong he thong
- app/** — Mini app (tru khi dang lam task UI)
- state/pipeline.db schema
- config/*.yaml schema

### NT3 — Publish qua pipeline, KHONG tu dang
CAM goi truc tiep: os_publish.publish(), multichannel_runner.publish_one_channel()

DUNG:
bash
python -m pipeline.runner --job-json '{"channel":"Mialinhcute",...}'


Agent DUOC tao job, KHONG duoc approve/publish (tru khi user ra lenh ro).

### NT4 — Moi module phai co MODULE dict + bump version
Khi sua 1 module, PHAI:
1. Bump MODULE["version"] (semver)
2. Them dong vao CHANGELOG.md
3. Chay python -m pipeline.selfcheck modules/<ten> -> PASS

Neu version moi fail benchmark -> rollback ve version truoc.

### NT5 — Selfcheck PASS truoc khi ket thuc phien
Truoc khi ket thuc, chay:
bash
python -m pipeline.selfcheck

Neu FAIL -> sua cho PASS hoac bao user.
KHONG ket thuc phien voi selfcheck FAIL.

### NT6 — Audit log moi thay doi
Moi lan sua file ngoai modules/, ghi vao bang audit:
- ai (agent/chat phien nao)
- sua file nao
- ly do
- version truoc/sau

## MOI TRUONG — WORKAROUND DA KIEM CHUNG

Trong mot so phien, tool bi loi mangle content:
- Strip moi ky tu * va __ (Markdown parsing)
- Gop 4-space indent -> 1 space
- Nuot backtick trong code block

Cach ghi file dang tin:
- Dung run_python voi list L=[]; A=L.append
- Indent bang chr(9) (TAB song sot), KHONG dung space
- Ky tu dac biet: chr(42) = *, chr(95) = _, chr(96) = backtick
- Verify ngay: ast.parse(open(path).read()) truoc khi chay

Cach doc file dang tin:
- repr(line) tung dong thay vi print(text)
- Hoacio.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")`

## QUY TRINH CHUAN MOT PHIEN


1. Doc STATE.md + PIPELINE_SPEC.md
2. Doc AGENT_RULES.md (file nay)
3. Query pipeline.db -> biet trang thai that
4. Chon 1 module de nang cap (hoac task user giao)
5. Sua trong modules/ -> bump version -> CHANGELOG
6. selfcheck modules/<ten> -> PASS
7. selfcheck (toan bo) -> PASS
8. Cap nhat STATE.md neu co thay doi lon
9. Viet PHIEN_HANDOFF.md cho phien sau


## NEU VI PHAM

Neu phat hien da vi pham 1 trong 6 nguyen tac tren:
1. DUNG ngay
2. Bao user ro rang
3. Rollback neu co the
4. Ghi vao audit

---

