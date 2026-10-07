import sys

from Crypto.Cipher import DES


PLAINTEXT_1 = b"STAYHOME"
PLAINTEXT_2 = b"STAYHOMA"
DEFAULT_KEYS = (b"87654321", b"12345678")


def hamming_distance(first, second):
    return sum((left ^ right).bit_count() for left, right in zip(first, second))


def avalanche_test(key):
    ciphertext_1 = DES.new(key, DES.MODE_ECB).encrypt(PLAINTEXT_1)
    ciphertext_2 = DES.new(key, DES.MODE_ECB).encrypt(PLAINTEXT_2)
    changed_bits = hamming_distance(ciphertext_1, ciphertext_2)
    total_bits = len(ciphertext_1) * 8

    print(f"Key: {key.decode()}")
    print(f"C1: {ciphertext_1.hex()} ({int.from_bytes(ciphertext_1, 'big'):064b})")
    print(f"C2: {ciphertext_2.hex()} ({int.from_bytes(ciphertext_2, 'big'):064b})")
    print(f"Hamming distance: {changed_bits}/{total_bits} bits")
    print(f"Changed ratio: {changed_bits / total_bits * 100:.2f}%")
    return changed_bits


def main():
    keys = tuple(argument.encode() for argument in sys.argv[1:]) or DEFAULT_KEYS
    if any(len(key) != DES.key_size for key in keys):
        raise SystemExit("Each key must be exactly 8 ASCII bytes")

    for key in keys:
        avalanche_test(key)
        print()


if __name__ == "__main__":
    main()
