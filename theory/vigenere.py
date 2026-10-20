
def vigenere(text, key, decrypt=False):
    key = key.upper()

    if not key or not key.isascii() or not key.isalpha():
        raise ValueError("Khoa phai chi chua chu cai A-Z!")

    result = ""
    j = 0

    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            base = ord('A') if char.isupper() else ord('a')

            p = ord(char) - base
            k = ord(key[j % len(key)]) - ord('A')

            if decrypt:
                c = (p - k) % 26
            else:
                c = (p + k) % 26

            result += chr(c + base)
            j += 1
        else:
            result += char

    return result


while True:
    print("\n===== VIGENERE CIPHER =====")
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
    key = input("Nhap khoa: ")

    try:
        if choice == "1":
            print("Ban ma:", vigenere(text, key))
        else:
            print("Ban ro:", vigenere(text, key, decrypt=True))
    except ValueError as e:
        print("Loi:", e)
