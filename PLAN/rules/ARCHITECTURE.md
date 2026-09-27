# KIẾN TRÚC 3 HỆ THỐNG ĐỘC LẬP — TNT MEDIA OS

Mục tiêu: tách bạch rõ source ≠ data ≠ release, tham chiếu MONOLUX.

## Ba hệ thống


PLAN/ -> bàn bạc, lên kế hoạch (KHÔNG chạy code, KHÔNG sửa source)
DEV/ -> sửa lỗi, nâng cấp (KHÔNG chạm runtime data, KHÔNG publish)
RUN/ -> quản lý và chạy trực tiếp (KHÔNG sửa source)


## PLAN/
- ROADMAP.md, BACKLOG.md, DECISIONS.md (ADR)
- HANDOFF/ — bàn giao từng phiên
- Đầu vào: trạng thái RUN/, lỗi từ DEV/
- Đầu ra: task cho DEV/

## DEV/
- src/ — source thật (pipeline, modules, app)
- tests/ — test cô lập, DB tạm
- rules/ — CODE_RULES.md, AGENT_EXECUTION_RULES.md
- Chỉ nhận task từ PLAN/
- Commit phải có test

## RUN/
- state/ — DB, WAL/SHM, config runtime
- output/ — video render
- logs/ — log
- backups/ — backup DB
- credentials/ — token (gitignore triệt để)
- app/ — entry point chạy (tray.py, server.py, scheduler, runner)

## Luật bất biến
1. PLAN không chạy code, không sửa source.
2. DEV không chạm runtime data.
3. RUN không sửa source.
4. Mọi thay đổi source qua DEV; mọi quyết định qua PLAN.
5. Không commit runtime data / secrets / media nặng vào Git.
