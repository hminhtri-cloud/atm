# ============================================================
# RAIL FENCE CIPHER
# ============================================================


def rail_fence_encrypt(plaintext, rails):
    # Kiểm tra số rail
    if rails < 2:
        raise ValueError("Number of rails must be at least 2.")

    # Nếu số rail >= độ dài text thì không cần mã hóa
    if rails >= len(plaintext):
        return plaintext

    # Tạo các hàng rỗng
    fence = [""] * rails

    current_rail = 0
    direction = 1

    # Đưa từng ký tự vào các rail theo đường zigzag
    for char in plaintext:

        fence[current_rail] += char

        # Chạm rail cuối -> đi lên
        if current_rail == rails - 1:
            direction = -1

        # Chạm rail đầu -> đi xuống
        elif current_rail == 0:
            direction = 1

        current_rail += direction

    # Ghép các rail lại để tạo ciphertext
    return "".join(fence)


def rail_fence_decrypt(ciphertext, rails):
    # Kiểm tra số rail
    if rails < 2:
        raise ValueError("Number of rails must be at least 2.")

    if rails >= len(ciphertext):
        return ciphertext

    # ========================================================
    # Bước 1: Xác định rail của từng vị trí
    # ========================================================

    pattern = []

    current_rail = 0
    direction = 1

    for _ in ciphertext:

        pattern.append(current_rail)

        if current_rail == rails - 1:
            direction = -1

        elif current_rail == 0:
            direction = 1

        current_rail += direction

    # ========================================================
    # Bước 2: Đếm số ký tự thuộc mỗi rail
    # ========================================================

    rail_lengths = [
        pattern.count(i)
        for i in range(rails)
    ]

    # ========================================================
    # Bước 3: Chia ciphertext trở lại từng rail
    # ========================================================

    rail_contents = []

    index = 0

    for length in rail_lengths:

        rail_contents.append(
            list(ciphertext[index:index + length])
        )

        index += length

    # ========================================================
    # Bước 4: Đi lại theo pattern zigzag để khôi phục plaintext
    # ========================================================

    rail_positions = [0] * rails

    plaintext = ""

    for rail in pattern:

        plaintext += rail_contents[rail][
            rail_positions[rail]
        ]

        rail_positions[rail] += 1

    return plaintext


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("RAIL FENCE CIPHER")
    print("=" * 60)

    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Test")

    choice = input("\nChoose: ").strip()

    try:

        # ====================================================
        # ENCRYPT
        # ====================================================

        if choice == "1":

            plaintext = input(
                "Enter plaintext: "
            )

            rails = int(
                input("Enter number of rails: ")
            )

            ciphertext = rail_fence_encrypt(
                plaintext,
                rails
            )

            print("\nCiphertext:")
            print(ciphertext)

        # ====================================================
        # DECRYPT
        # ====================================================

        elif choice == "2":

            ciphertext = input(
                "Enter ciphertext: "
            )

            rails = int(
                input("Enter number of rails: ")
            )

            plaintext = rail_fence_decrypt(
                ciphertext,
                rails
            )

            print("\nPlaintext:")
            print(plaintext)

        # ====================================================
        # TEST
        # ====================================================

        elif choice == "3":

            TEST_FILE = "rail_fence.txt"
            rails = 3

            # Đọc plaintext từ file
            with open(TEST_FILE, "r", encoding="utf-8") as file:
                plaintext = file.read()

            # Mã hóa
            ciphertext = rail_fence_encrypt(
                plaintext,
                rails
            )

            # Giải mã lại
            decrypted = rail_fence_decrypt(
                ciphertext,
                rails
            )

            print("\n" + "=" * 60)
            print("RAIL FENCE TEST")
            print("=" * 60)

            print("\nOriginal Plaintext:")
            print(plaintext)

            print("\nNumber of Rails:")
            print(rails)

            print("\nCiphertext:")
            print(ciphertext)

            print("\nDecrypted Text:")
            print(decrypted)

            print("\n" + "=" * 60)

            if decrypted == plaintext:
                print("[PASS] Decrypted text matches original plaintext.")
            else:
                print("[FAIL] Decrypted text does not match original plaintext.")

        else:
            print("Invalid choice.")

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()