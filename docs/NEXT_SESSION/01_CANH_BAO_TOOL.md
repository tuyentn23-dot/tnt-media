# CANH BAO KY THUAT (PHAI DOC TRUOC)

## 0.1. Tool write_file STRIP dau gach duoi kep (__)
Moi lan ghi file Python qua write_file, __ bi mat.

Bat buoc dung placeholder + patch:
- FILEMARK -> __file__
- MAINMARK -> __main__
- INITMARK -> __init__

Quy trinh:
1. write_file voi placeholder
2. python ops/_patch.py <path>
3. python -c "import ast; ast.parse(open('<path>').read()); print('OK')"

## 0.2. Tool write_file STRIP * trong string literal
Tranh viet chr(9)*3. Dung bien:

T1 = chr(9)
T3 = T1 + T1 + T1


## 0.3. Tool output CAT o ~1500 ky tu
Doc file dai phai doc tung doan:
python ops/_tmp_dump.py <path> <start> <end>

## 0.4. Tool output doi khi UTF-16/CP1252
Ep UTF-8:
python
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


## 0.5. File ghi ra 0 bytes khi qua dai
Neu write_file content > ~5000 ky tu co the ghi 0 bytes.
Chia nho file, moi file < 3000 ky tu.

## 0.6. PowerShell khong ho tro &&
Dung ; hoac chay lenh rieng.

## 0.7. Lenh chay nen
cmd /c start /B python -m pipeline.runner ... > logs\_x.log 2>&1
Sau do Start-Sleep + doc log.
