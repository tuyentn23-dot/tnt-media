# RUNTIME RULES — RUN

1. RUN không sửa source; chỉ vận hành.
2. Dữ liệu runtime nằm trong RUN/state, RUN/output, RUN/logs, RUN/backups, RUN/credentials.
3. credentials/ gitignore triệt để; không log token.
4. Không bật scheduler production khi test; dùng cổng riêng, DB cách ly.
5. Backup DB trước thao tác rủi ro.
6. Tray/server là entry point của RUN; không dispatch job ngoài phạm vi test.
