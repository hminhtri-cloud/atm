# Nhiệm vụ 2.6
# Viết một chương trình (bằng ngôn ngữ lập trình của bạn) để đáp ứng các yêu cầu
# sau:
# 1. Số nguyên tố:
# • Tạo ra một số nguyên tố ngẫu nhiên có 8 bits, 16 bits, 64 bits
# • Xác định 10 số nguyên tố lớn nhất nhỏ hơn số nguyên tố Mersenne thứ 10.
# • Kiểm tra xem một số nguyên tùy ý nhỏ hơn 289
# − 1 có phải là số nguyên
# tố hay không?
# 2. Xác định ước số chung lớn nhất (GCD) của 2 số nguyên lớn tùy ý (lớn nhất
# có thể mà bạn có thể xử lý).
# 3. Tính toán lũy thừa theo module ax mod p. Chương trình của bạn phải có khả
# năng tính toán trong trường hợp số mũ lớn (x>40), ví dụ, 740 mod 19

# • Để kiểm tra các số nguyên tố lớn (Mersenne Prime), bạn có thể tìm hiểu và
# sử dụng thuật toán Miller-Rabin.
# • Để xác định ước số chung lớn nhất (greatest common divisor), bạn nên sử
# dụng thuật toán Euclid.
# • Phép nhân module có tính chất sau:
# (a × b) ≡ [(a mod n) × (b mod n)] mod n
# Tính chất này có thể được áp dụng để tính toán lũy thừa module (modular
# exponentiation) trong trường hợp có số mũ lớn.

from Crypto.Util.number import getPrime

import random

def my_miller_rabin(n, k=10):
    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    # Phân tích n - 1 = 2^s * d
    s = 0
    d = n - 1

    while d % 2 == 0:
        s += 1
        d //= 2

    # Thực hiện k vòng kiểm tra
    for _ in range(k):
        a = random.randrange(2, n - 1)

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True

def is_prime(n):
    if n < 2:
        return False
    if n < 10000000:
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    else:
        return my_miller_rabin(n)

def list_primes_less_than_mersenne_prime(n):
    # Tìm số nguyên tố Mersenne thứ n
    mersenne_prime = (1 << n) - 1  # 2^n - 1

    # Tìm các số nguyên tố nhỏ hơn số nguyên tố Mersenne thứ n
    primes = []
    count = 10
    while count > 0:
        mersenne_prime -= 1
        if is_prime(mersenne_prime):
            primes.append(mersenne_prime)
            count -= 1

    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modular_exponentiation(a, x, p):
    result = 1
    a = a % p

    while x > 0:
        if (x % 2) == 1:
            result = (result * a) % p
        x = x >> 1
        a = (a * a) % p

    return result

def main():
    #Tạo ra một số nguyên tố ngẫu nhiên có 8 bits, 16 bits, 64 bits
    prime8 = getPrime(8)
    prime16 = getPrime(16)
    prime64 = getPrime(64)

    print("Số nguyên tố 8 bits:", prime8)
    print("Số nguyên tố 16 bits:", prime16)
    print("Số nguyên tố 64 bits:", prime64)

    #Xác định 10 số nguyên tố lớn nhất nhỏ hơn số nguyên tố Mersenne thứ 10.
    primes_less_than_mersenne = list_primes_less_than_mersenne_prime(10)
    print("10 số nguyên tố lớn nhất nhỏ hơn số nguyên tố Mersenne thứ 10:", primes_less_than_mersenne)

    #Kiểm tra xem một số nguyên tùy ý nhỏ hơn 2^89 - 1 có phải là số nguyên tố hay không?
    test_number = int(input("Nhập một số nguyên nhỏ hơn 2^89 - 1 để kiểm tra xem nó có phải là số nguyên tố không: "))
    if test_number >= (1 << 89) - 1:
        print("Số nhập vào phải nhỏ hơn 2^89 - 1.")
    else:
        if is_prime(test_number):
            print(f"{test_number} là số nguyên tố.")
        else:
            print(f"{test_number} không phải là số nguyên tố.")

    #2. Xác định ước số chung lớn nhất (GCD) của 2 số nguyên lớn tùy ý (lớn nhất có thể mà bạn có thể xử lý).
    num1 = int(input("Nhập số nguyên thứ nhất: "))
    num2 = int(input("Nhập số nguyên thứ hai: "))
    print(f"Ước số chung lớn nhất của {num1} và {num2} là: {gcd(num1, num2)}")

    #3. Tính toán lũy thừa theo module ax mod p. Chương trình của bạn phải có khả năng tính toán trong trường hợp số mũ lớn (x>40), ví dụ, 740 mod 19
    a = int(input("Nhập số nguyên a: "))
    x = int(input("Nhập số mũ x: "))
    p = int(input("Nhập số nguyên p: "))
    print(f"{a}^{x} mod {p} = {modular_exponentiation(a, x, p)}")

if __name__ == "__main__":
    main()

