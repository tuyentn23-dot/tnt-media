# TNT WRAPPER RULES - doc ky truoc khi ghi file

## write_file
- NUOT: __ (gach duoi kep) -> dung env/cwd thay file
- NUOT: * (dau nhan) -> luon co SPACE quanh *
- PHA indent: 4 space -> 1 space. Moi cap indent = 1 space.

## run_python
- NUOT: __ giong write_file
- PHA: escape 
 trong string -> dung chr(10)
- NUOT: * khi +so KHONG space (hh3600 -> hh3600) -> luon SPACE quanh 
- Giu indent 1-space neu nhat quan

## QUY TAC VIET CODE AN TOAN
- Dung chr(10) cho newline, chr(39) cho quote don, chr(34) cho quote kep
- Tranh moi x (file, name, init)
- Tranh block long > 1 cap (if trong for trong def = HONG)
- Thay if/for long bang: comprehension, next(gen, default), bieu thuc 3 ngoi
- Thay file bang os.environ.get(ROOT) hoac os.getcwd() hoac sys.path scan
- Luon SPACE quanh dau * : a * b KHONG viet ab khi b la so nhieu chu so
- File > 1274 bytes: ghi bang run_python list-join, khong dung write_file

## BAI HOC QUAN TRONG
- KHONG dung s.find("def X") de XOA ham - neu X o giua file, se xoa het ham sau no!
 -> Luon kiem tra i1 (bat dau) VA i2 (ham ke tiep) truoc khi cat.
- Quy luat dau * : * bi nuot khi * + so/chu KHONG co space VA dung sau ky tu khong-space.
 -> LUON co space quanh * : a * b (vd: 0.66 * h, hh * 3600)
- Trong ffmpeg filter, space quanh * OK (da test).
- FFmpeg filter_complex: label output cuoi phai la [v] de -map [v].
- Audio index dong: [N:a] voi N = so video input.

## GIAI PHAP INDENT: DUNG TAB!
- run_python GIU NGUYEN tab (chr(9)) va nhieu cap tab (chr(9)+chr(9)).
- => Dung tab cho MOI file co block long (try/except, for/if, def trong def).
- LUU Y: khong tron tab va space trong cung file (Python cam).
- File dung tab: footage_fetcher.py (mau chuan).
- File dung space (1-space): cac file phang khong block long.
