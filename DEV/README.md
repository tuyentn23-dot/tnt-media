# DEV/ — Khu vực phát triển

Vai trò: sửa lỗi, nâng cấp source. KHÔNG chạm runtime data, KHÔNG publish.

## Nội dung thuộc DEV
- src/pipeline/ — orchestration (HARD module)
- src/modules/ — content/render/voice/publish modules
- src/app/ — FastAPI server, tray, routes
- src/ops/ — thao tác ffmpeg/voice/publish + _no_window.py
- src/os_app/, src/analytics/
- tests/ — test cô lập (DB tạm, cổng riêng)
- scripts/, tools/, deploy/
- rules/CODE_RULES.md, rules/AGENT_EXECUTION_RULES.md

## Quy tắc
1. Mọi commit phải kèm test.
2. Test cô lập production (DB tạm, không bật scheduler production).
3. Không hard-code đường dẫn máy; dùng hằng số tập trung.
4. Không hạ tiêu chuẩn để đạt PASS.

## Lệnh test chuẩn

python tests/p0_check.py # 21 PASS / 0 FAIL
python -m pipeline.selfcheck # 27 PASS / 0 FAIL
python tests/ui_accept.py # TITLE, TABS 13, JS_ERRORS []


## Trạng thái di chuyển
Source hiện VẪN ở gốc workspace. Kế hoạch di chuyển: xem PLAN/MIGRATION_PLAN.md giai đoạn 2.
