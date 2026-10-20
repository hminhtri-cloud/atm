
from math import gcd
last_ciphertext = None


# Kiem tra so nguyen to
def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


# Tao cap khoa RSA
def generate_keys(p, q):
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p va q phai la so nguyen to!")

    if p == q:
        raise ValueError("p va q phai khac nhau!")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Chon so mu cong khai e
    e = 65537

    if e >= phi or gcd(e, phi) != 1:
        e = 3
        while e < phi and gcd(e, phi) != 1:
            e += 2

    if e >= phi:
        raise ValueError("Khong tim duoc khoa e!")

    # Tim nghich dao modulo
    d = pow(e, -1, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key, phi


# Ma hoa RSA
def rsa_encrypt(text, public_key):
    e, n = public_key

    data = text.encode("utf-8")

    if n <= 255:
        raise ValueError("n phai lon hon 255!")

    ciphertext = []

    for byte in data:
        c = pow(byte, e, n)
        ciphertext.append(c)

    return ciphertext


# Giai ma RSA
def rsa_decrypt(ciphertext, private_key):
    d, n = private_key

    plaintext = []

    for c in ciphertext:
        if not (0 <= c < n):
            raise ValueError("Gia tri ban ma khong hop le!")

        m = pow(c, d, n)

        if not (0 <= m <= 255):
            raise ValueError("Byte giai ma khong hop le!")

        plaintext.append(m)

    return bytes(plaintext).decode("utf-8")


# Chuong trinh chinh
public_key = None
private_key = None

while True:
    print("\n===== RSA CIPHER =====")
    print("1. Tao cap khoa RSA")
    print("2. Ma hoa")
    print("3. Giai ma")
    print("4. Giai ma tu ban ma cu")
    print("0. Thoat")

    choice = input("Chon chuc nang: ")

    if choice == "0":
        break

    try:
        if choice == "1":
            p = int(input("Nhap so nguyen to p: "))
            q = int(input("Nhap so nguyen to q: "))

            public_key, private_key, phi = (
                generate_keys(p, q)
            )

            print("\n===== THONG TIN KHOA =====")
            print("p =", p)
            print("q =", q)
            print("n =", p * q)
            print("phi(n) =", phi)
            print("Public Key:", public_key)
            print("Private Key:", private_key)

        elif choice == "2":
            if public_key is None:
                print("Vui long tao khoa truoc!")
                continue

            text = input("Nhap ban ro: ")
            result = rsa_encrypt(text, public_key)
            last_ciphertext = result

            print("Ban ma:", result)

        elif choice == "3":
            if private_key is None:
                print("Vui long tao khoa truoc!")
                continue

            text = input(
                "Nhap ban ma (cac so cach nhau boi dau phay): "
            )

            ciphertext = list( map(int, text.replace(",", " ").replace("[", "").replace("]", "").split()))
            result = rsa_decrypt(
                ciphertext, private_key
            )

            print("Ban ro:", result)

        elif choice == "4":
            if last_ciphertext is None:
                print("Chua co ban ma de giai ma!")
                continue

            result = rsa_decrypt(
                last_ciphertext, private_key
            )

            print("Ban ro:", result)
        else:
            print("Lua chon khong hop le!")

    except (ValueError, UnicodeDecodeError) as e:
        print("Loi:", e)
