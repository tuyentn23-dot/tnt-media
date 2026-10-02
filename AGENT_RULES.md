# AGENT_RULES - Quy tac bat buoc cho AI agent

## TRUOC KHI LAM
1. Doc guardian/README.md
2. Chay: python guardian/guard.py before (snapshot)

## TRONG KHI LAM
- KHONG dung os.remove / Remove-Item / rm truc tiep
- Xoa file: python guardian/safe_fs.py remove <file>
- Khong xoa hang loat (glob + remove)
- Dung absolute path hoac cd dung workspace
- Kiem tra git status truoc khi thao tac file

## SAU KHI LAM XONG
1. Chay: python guardian/guard.py verify
2. Commit neu co thay doi quan trong

## NEU FILE QUAN TRONG BI MAT
- Chay: python guardian/snapshot.py restore

## LUU Y TOOL PHIEN NAY
- write_file/run_python hay PHA code (nuot ky tu dac biet)
- Cach chong: dung base64 hoac build bang chr()
- cwd hay doi ve D:/TNT_AI -> luon cd ve workspace
- Khong kill python (se tu kill tool)
