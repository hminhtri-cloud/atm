
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib


# Tao khoa AES-256 tu mat khau va salt
def create_key(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000,
        dklen=32
    )


# Ma hoa AES-256-GCM
def aes_encrypt(text, password):
    salt = get_random_bytes(16)
    key = create_key(password, salt)

    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(
        text.encode("utf-8")
    )

    # Luu salt + nonce + tag + ciphertext
    data = salt + cipher.nonce + tag + ciphertext

    return base64.b64encode(data).decode("utf-8")


# Giai ma AES-256-GCM
def aes_decrypt(encrypted_text, password):
    data = base64.b64decode(
        encrypted_text,
        validate=True
    )

    if len(data) < 48:
        raise ValueError("Du lieu ma hoa khong hop le!")

    salt = data[:16]
    nonce = data[16:32]
    tag = data[32:48]
    ciphertext = data[48:]

    key = create_key(password, salt)

    cipher = AES.new(
        key,
        AES.MODE_GCM,
        nonce=nonce
    )

    plaintext = cipher.decrypt_and_verify(
        ciphertext, tag
    )

    return plaintext.decode("utf-8")


# Chuong trinh chinh
while True:
    print("\n===== AES-256-GCM =====")
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
    password = input("Nhap mat khau: ")

    if not password:
        print("Mat khau khong duoc de trong!")
        continue

    try:
        if choice == "1":
            result = aes_encrypt(text, password)
            print("\nBan ma:", result)

        else:
            result = aes_decrypt(text, password)
            print("\nBan ro:", result)

    except (ValueError, UnicodeDecodeError) as e:
        print("Giai ma that bai!")
        print("Sai mat khau hoac du lieu bi thay doi.")
