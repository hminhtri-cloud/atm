# Lab 02

## Chay chuong trinh

Cai thu vien:

```bash
python3 -m pip install pycryptodome
```

Chay tung task:

```bash
python3 c1/c1.py
python3 c2/c2.py
python3 c3/c3.py
python3 c5/c5.py
```

Task 3 cho phep truyen cac key DES dai 8 ky tu, vi du ma so sinh vien:

```bash
python3 c3/c3.py 87654321 12345678
```

## Task 5

Du lieu gom 1000 byte, byte thu 26 duoc dao bit dau tien. ECB va OFB lam hong
mot khoi plaintext; CBC va CFB (segment 128 bit) lam hong khoi hien tai va
khoi ke tiep. CFB/OFB khong tu dong padding trong ung dung thuc te; script
pad du lieu de ECB va CBC co the xu ly cung mot dau vao.
