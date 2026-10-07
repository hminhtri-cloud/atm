def F(right, subkey):
    return (right ^ subkey) & 0x0F


def feistel_round(left_in, right_in, subkey):
    left_out = right_in
    right_out = left_in ^ F(right_in, subkey)
    return left_out & 0x0F, right_out & 0x0F


def track_avalanche(message, key):
    left = (message >> 4) & 0x0F
    right = message & 0x0F
    subkeys = [
        key & 0x0F,
        (key >> 4) & 0x0F,
        (key + 1) & 0x0F,
        (key + 2) & 0x0F,
    ]

    print(f"Khoi tao: L={left:04b}, R={right:04b}")
    for index, subkey in enumerate(subkeys, start=1):
        left, right = feistel_round(left, right, subkey)
        print(f"Vong {index}: L={left:04b}, R={right:04b}")
    return (left << 4) | right


if __name__ == "__main__":
    print("--- Ma hoa M1 ---")
    result_1 = track_avalanche(0xAB, 0x12)
    print(f"Ciphertext M1: 0x{result_1:02X}")

    print("--- Ma hoa M2 ---")
    result_2 = track_avalanche(0xAC, 0x12)
    print(f"Ciphertext M2: 0x{result_2:02X}")
    print(f"So bit khac nhau: {(result_1 ^ result_2).bit_count()}")
