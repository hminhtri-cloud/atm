
from math import gcd

# Tinh nghich dao modulo 26
def mod_inverse(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Khong ton tai nghich dao modulo!")


# Kiem tra va tim ma tran khoa nghich dao
def inverse_matrix(K):
    a, b = K[0]
    c, d = K[1]

    det = (a * d - b * c) % 26

    if gcd(det, 26) != 1:
        raise ValueError("Ma tran khoa khong kha nghich!")

    det_inv = mod_inverse(det)

    return [
        [(d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, (a * det_inv) % 26]
    ]


# Chuan hoa van ban
def prepare_text(text):
    return ''.join(
        char for char in text.upper()
        if 'A' <= char <= 'Z'
    )


# Ma hoa Hill
def hill_encrypt(text, K):
    inverse_matrix(K)  # Kiem tra khoa

    text = prepare_text(text)

    if len(text) % 2 != 0:
        text += 'X'

    result = ""

    for i in range(0, len(text), 2):
        p1 = ord(text[i]) - 65
        p2 = ord(text[i + 1]) - 65

        c1 = (K[0][0] * p1 + K[0][1] * p2) % 26
        c2 = (K[1][0] * p1 + K[1][1] * p2) % 26

        result += chr(c1 + 65) + chr(c2 + 65)

    return result


# Giai ma Hill
def hill_decrypt(text, K):
    K_inv = inverse_matrix(K)
    text = prepare_text(text)

    if len(text) % 2 != 0:
        raise ValueError("Ban ma phai co do dai chan!")

    result = ""

    for i in range(0, len(text), 2):
        c1 = ord(text[i]) - 65
        c2 = ord(text[i + 1]) - 65

        p1 = (K_inv[0][0] * c1 + K_inv[0][1] * c2) % 26
        p2 = (K_inv[1][0] * c1 + K_inv[1][1] * c2) % 26

        result += chr(p1 + 65) + chr(p2 + 65)

    return result


# Chuong trinh chinh
while True:
    print("\n===== HILL CIPHER =====")
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
        print("Nhap ma tran khoa 2x2:")
        a, b = map(int, input("Hang 1: ").split())
        c, d = map(int, input("Hang 2: ").split())

        K = [[a, b], [c, d]]

        text = input("Nhap van ban: ")

        if choice == "1":
            print("Ban ma:", hill_encrypt(text, K))
        else:
            print("Ban ro:", hill_decrypt(text, K))

    except ValueError as e:
        print("Loi:", e)
