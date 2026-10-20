
import secrets


# Kiem tra so nguyen to
def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


# Tim cac uoc nguyen to cua n
def prime_factors(n):
    factors = set()
    d = 2

    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1

    if n > 1:
        factors.add(n)

    return factors


# Kiem tra g la phan tu sinh modulo p
def is_generator(g, p):
    if not (1 < g < p):
        return False

    for q in prime_factors(p - 1):
        if pow(g, (p - 1) // q, p) == 1:
            return False

    return True


# Mo phong Diffie-Hellman
def diffie_hellman(p, g):
    if not is_prime(p) or p < 5:
        raise ValueError("p phai la so nguyen to >= 5!")

    if not is_generator(g, p):
        raise ValueError(
            "g phai la phan tu sinh modulo p!"
        )

    # Tao khoa bi mat
    a = secrets.randbelow(p - 3) + 2
    b = secrets.randbelow(p - 3) + 2

    # Tinh khoa cong khai
    A = pow(g, a, p)
    B = pow(g, b, p)

    # Tinh khoa bi mat chung
    K_A = pow(B, a, p)
    K_B = pow(A, b, p)

    print("\n===== ALICE =====")
    print("Khoa bi mat a:", a)
    print("Khoa cong khai A:", A)

    print("\n===== BOB =====")
    print("Khoa bi mat b:", b)
    print("Khoa cong khai B:", B)

    print("\n===== TRAO DOI KHOA =====")
    print("Alice gui A =", A, "cho Bob")
    print("Bob gui B =", B, "cho Alice")

    print("\n===== KET QUA =====")
    print("Khoa chung Alice:", K_A)
    print("Khoa chung Bob:", K_B)

    if K_A == K_B:
        print("Trao doi khoa thanh cong!")
    else:
        print("Trao doi khoa that bai!")


# Chuong trinh chinh
while True:
    print("\n===== DIFFIE-HELLMAN =====")
    print("1. Mo phong trao doi khoa")
    print("0. Thoat")

    choice = input("Chon chuc nang: ")

    if choice == "0":
        break

    if choice != "1":
        print("Lua chon khong hop le!")
        continue

    try:
        p = int(input("Nhap so nguyen to p: "))
        g = int(input("Nhap phan tu sinh g: "))

        diffie_hellman(p, g)

    except ValueError as e:
        print("Loi:", e)
