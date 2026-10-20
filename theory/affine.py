
from math import gcd


# Tim nghich dao modulo
def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Khong ton tai nghich dao modulo!")


# Kiem tra khoa
def check_key(a, b):
    if gcd(a, 26) != 1:
        raise ValueError(
            "Khoa a phai nguyen to cung nhau voi 26!"
        )


# Ma hoa Affine
def affine_encrypt(text, a, b):
    check_key(a, b)
    result = ""

    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            base = ord('A') if char.isupper() else ord('a')
            p = ord(char) - base

            c = (a * p + b) % 26

            result += chr(c + base)
        else:
            result += char

    return result


# Giai ma Affine
def affine_decrypt(text, a, b):
    check_key(a, b)
    a_inv = mod_inverse(a)
    result = ""

    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base

            p = (a_inv * (c - b)) % 26

            result += chr(p + base)
        else:
            result += char

    return result


# Chuong trinh chinh
while True:
    print("\n===== AFFINE CIPHER =====")
    print("1. Ma hoa")
    print("2. Giai ma")
    print("0. Thoat")

    choice = input("Chon chuc nang: ")

    if choice == "0":
        break

    if choice not in ("1", "2"):
        print("Lua chon khong hop le!")
        continue

    try:
        a = int(input("Nhap khoa a: "))
        b = int(input("Nhap khoa b: "))

        text = input("Nhap van ban: ")

        if choice == "1":
            print("Ban ma:", affine_encrypt(text, a, b))
        else:
            print("Ban ro:", affine_decrypt(text, a, b))

    except ValueError as e:
        print("Loi:", e)
