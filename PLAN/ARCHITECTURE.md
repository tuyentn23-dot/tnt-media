# KIẾN TRÚC ĐÍCH — TNT MEDIA OS (3 hệ thống độc lập)

Nguyên tắc bất biến: source ≠ data ≠ release.


PLAN/ -> bàn bạc, lên kế hoạch (KHÔNG chạy code, KHÔNG sửa source)
DEV/ -> sửa lỗi, nâng cấp (KHÔNG chạm runtime data, KHÔNG publish)
RUN/ -> quản lý và chạy trực tiếp (KHÔNG sửa source)


## Phân loại hiện trạng workspace (media/)

### -> DEV/ (source, product rules, tests)
| Hiện tại | Đích |
|---|---|
| pipeline/ | DEV/src/pipeline/ |
| modules/ | DEV/src/modules/ |
| app/ (server.py, tray.py, _routes_publish.py) | DEV/src/app/ |
| ops/ | DEV/src/ops/ |
| os_app/ | DEV/src/os_app/ |
| src/ | DEV/src/ |
| scripts/ | DEV/scripts/ |
| tests/ | DEV/tests/ |
| analytics/ | DEV/src/analytics/ |
| deploy/ | DEV/deploy/ |
| docs/ | PLAN/docs/ |
| tools/ | DEV/tools/ |

### -> RUN/ (runtime data, KHÔNG commit)
| Hiện tại | Đích |
|---|---|
| state/ (DB, WAL, config runtime) | RUN/state/ |
| output/ (video render) | RUN/output/ |
| logs/ | RUN/logs/ |
| backups/ | RUN/backups/ |
| work/ (render scratch) | RUN/work/ |
| cloud_media/ | RUN/cloud_media/ |
| library/ | RUN/library/ |
| music_bank/ | RUN/music_bank/ |
| movies/ | RUN/movies/ |
| memory/ (token, cache) | RUN/memory/ |
| config/ (client_secrets, token) | RUN/credentials/ |
| channels/ (/token.pickle) | RUN/credentials/channels/ |
| _trash/, _attic/, _archive/ | RUN/_attic/ |

### -> PLAN/ (docs, quyết định)
- ROADMAP.md, BACKLOG.md, DECISIONS.md, ARCHITECTURE.md, MIGRATION_PLAN.md
- HANDOFF/
- rules/ARCHITECTURE.md
- docs/ (từ gốc)

## Entry points sau tái cấu trúc
- RUN: RUN/app/tray.py, RUN/app/server.py, scheduler, runner
- DEV: source thật + tests
- Đường dẫn DB: RUN/state/pipeline.db
- Đường dẫn credentials: RUN/credentials/

## Nguyên tắc di chuyển an toàn
1. Dừng mọi tiến trình app trước khi di chuyển.
2. Backup DB trước.
3. Di chuyển từng nhóm, chạy test sau mỗi nhóm.
4. Cập nhật sys.path + hằng số đường dẫn tập trung (1 nơi).
5. Không commit runtime data.
6. Rollback nếu test fail.
