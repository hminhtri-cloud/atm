
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


# Kiem tra khoa DES
def check_key(key):
    key = key.encode("utf-8")

    if len(key) != 8:
        raise ValueError("Khoa DES phai co dung 8 byte!")

    return key


# Ma hoa DES
def des_encrypt(text, key):
    key = check_key(key)

    # Tao IV ngau nhien 8 byte
    iv = get_random_bytes(8)

    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv=iv
    )

    # Chuyen van ban thanh bytes va padding
    plaintext = text.encode("utf-8")
    padded_text = pad(plaintext, DES.block_size)

    # Ma hoa
    ciphertext = cipher.encrypt(padded_text)

    # Ghep IV va ban ma
    data = iv + ciphertext

    return base64.b64encode(data).decode("utf-8")


# Giai ma DES
def des_decrypt(encrypted_text, key):
    key = check_key(key)

    # Chuyen Base64 thanh bytes
    data = base64.b64decode(
        encrypted_text,
        validate=True
    )

    if len(data) < 16 or (len(data) - 8) % 8 != 0:
        raise ValueError("Ban ma khong hop le!")

    # Tach IV va ban ma
    iv = data[:8]
    ciphertext = data[8:]

    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv=iv
    )

    # Giai ma va loai bo padding
    padded_text = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_text, DES.block_size)

    return plaintext.decode("utf-8")


# Chuong trinh chinh
while True:
    print("\n===== DES CIPHER =====")
    print("1. Ma hoa")
    print("2. Giai ma")
    print("0. Thoat")

    choice = input("Chon chuc nang: ")

    if choice == "0":
        break

    if choice not in ("1", "2"):
        print("Lua chon khong hop le!")
        continue

    text = input("Nhap van ban: ")
    key = input("Nhap khoa (8 byte): ")

    try:
        if choice == "1":
            result = des_encrypt(text, key)
            print("\nBan ma:", result)

        else:
            result = des_decrypt(text, key)
            print("\nBan ro:", result)

    except (ValueError, UnicodeDecodeError) as e:
        print("Loi:", e)
