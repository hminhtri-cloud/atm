from Crypto.Cipher import AES


KEY = b"1234567890123456"
IV = b"6543210987654321"
DATA_SIZE = 1000
BYTE_TO_FLIP = 25  # The 26th byte, using zero-based indexing.
BLOCK_SIZE = AES.block_size


def pkcs7_pad(data):
    padding_length = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding_length]) * padding_length


def corrupted_block_count(original, recovered):
    return sum(
        original[offset:offset + BLOCK_SIZE] != recovered[offset:offset + BLOCK_SIZE]
        for offset in range(0, len(original), BLOCK_SIZE)
    )


def run_mode(name, data, damaged_ciphertext):
    if name == "ECB":
        cipher = AES.new(KEY, AES.MODE_ECB)
    elif name == "CBC":
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
    elif name == "CFB":
        cipher = AES.new(KEY, AES.MODE_CFB, IV, segment_size=128)
    elif name == "OFB":
        cipher = AES.new(KEY, AES.MODE_OFB, IV)
    else:
        raise ValueError(f"Unsupported mode: {name}")

    recovered = cipher.decrypt(damaged_ciphertext)[:DATA_SIZE]
    return corrupted_block_count(data, recovered), recovered


def encrypt(name, padded_data):
    if name == "ECB":
        cipher = AES.new(KEY, AES.MODE_ECB)
    elif name == "CBC":
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
    elif name == "CFB":
        cipher = AES.new(KEY, AES.MODE_CFB, IV, segment_size=128)
    elif name == "OFB":
        cipher = AES.new(KEY, AES.MODE_OFB, IV)
    else:
        raise ValueError(f"Unsupported mode: {name}")
    return cipher.encrypt(padded_data)


def main():
    data = bytes(index % 256 for index in range(DATA_SIZE))
    padded_data = pkcs7_pad(data)

    for mode in ("ECB", "CBC", "CFB", "OFB"):
        ciphertext = bytearray(encrypt(mode, padded_data))
        ciphertext[BYTE_TO_FLIP] ^= 0x01
        damaged_blocks, _ = run_mode(mode, data, bytes(ciphertext))
        print(f"{mode}: {damaged_blocks} corrupted plaintext block(s)")


if __name__ == "__main__":
    main()
