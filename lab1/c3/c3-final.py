import random
import math


# ============================================================
# CONFIG
# ============================================================

CIPHERTEXT_FILE = "c3.txt"
OUTPUT_FILE = "c3_output.txt"
TRIGRAM_FILE = "../english_trigrams.txt"

MAX_ITERATIONS = 20000
MAX_NO_IMPROVEMENT = 2000
NUM_RESTARTS = 50


# ============================================================
# 1. NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    """
    Chuyển văn bản về chữ thường và chỉ giữ lại a-z.
    Dùng cho quá trình tính trigram score.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    return ''.join(
        char for char in text.lower()
        if char in alphabet
    )


# ============================================================
# 2. DECRYPT
# ============================================================

def decrypt(ciphertext, key):

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    key = key.lower()

    result = ""

    for char in ciphertext:

        lower_char = char.lower()

        if lower_char in alphabet:

            # Tìm ciphertext character nằm ở đâu trong key
            pos = key.find(lower_char)

            # Chuyển về plaintext character tương ứng
            plain_char = alphabet[pos]

            # Giữ kiểu chữ hoa/thường nếu cần
            if char.isupper():
                plain_char = plain_char.upper()

            result += plain_char

        else:
            # Giữ nguyên khoảng trắng, dấu câu, newline...
            result += char

    return result


# ============================================================
# 3. LOAD ENGLISH TRIGRAM DATA
# ============================================================

def load_trigram_data(filename):
    """
    Đọc file dạng:

        THE 77534223
        AND 30997177
        ING 30679488
        ...

    Sau đó chuyển count thành log10 probability.

    Trả về:
        log_probability
        penalty
    """

    counts = {}

    # -------------------------
    # Đọc frequency
    # -------------------------

    with open(filename, "r") as f:

        for line in f:

            parts = line.split()

            if len(parts) != 2:
                continue

            trigram = parts[0].lower()
            count = int(parts[1])

            counts[trigram] = count

    # -------------------------
    # Tổng số trigram
    # -------------------------

    total = sum(counts.values())

    # -------------------------
    # Count -> log probability
    # -------------------------

    log_probability = {}

    for trigram, count in counts.items():

        probability = count / total

        log_probability[trigram] = math.log10(probability)

    # -------------------------
    # Penalty cho trigram
    # không có trong dataset
    # -------------------------

    penalty = math.log10(0.1 / total)

    return log_probability, penalty


# ============================================================
# 4. SCORE TEXT
# ============================================================

def score_text(text, log_probability, penalty):
    """
    Đánh giá mức độ giống tiếng Anh bằng trigram.

    Score càng cao -> càng giống tiếng Anh.
    """

    normalized = normalize_text(text)

    num_trigrams = len(normalized) - 2

    # Không đủ ký tự để tạo trigram
    if num_trigrams <= 0:
        return penalty

    score = 0.0

    # -------------------------
    # Duyệt từng trigram
    # -------------------------

    for i in range(num_trigrams):

        trigram = normalized[i:i + 3]

        if trigram in log_probability:
            score += log_probability[trigram]

        else:
            score += penalty

    # Lấy score trung bình
    return score / num_trigrams


# ============================================================
# 5. RANDOM KEY
# ============================================================

def random_key():
    """
    Tạo một substitution key ngẫu nhiên.
    """

    alphabet = list("abcdefghijklmnopqrstuvwxyz")

    random.shuffle(alphabet)

    return ''.join(alphabet)


# ============================================================
# 6. MUTATE KEY
# ============================================================

def mutate_key(key):
    """
    Tạo neighbor key bằng cách swap
    hai vị trí ngẫu nhiên.
    """

    key_list = list(key)

    idx1, idx2 = random.sample(range(26), 2)

    key_list[idx1], key_list[idx2] = \
        key_list[idx2], key_list[idx1]

    return ''.join(key_list)


# ============================================================
# 7. HILL CLIMBING
# ============================================================

def solve_cipher(
    ciphertext,
    log_probability,
    penalty,
    max_iterations=MAX_ITERATIONS
):
    """
    Thực hiện một lần Hill Climbing.

    Random key
        ↓
    Decrypt
        ↓
    Score
        ↓
    Mutate key
        ↓
    Better?
      Yes -> accept
      No  -> reject
    """

    # -------------------------
    # Random initial key
    # -------------------------

    current_key = random_key()

    current_plaintext = decrypt(
        ciphertext,
        current_key
    )

    current_score = score_text(
        current_plaintext,
        log_probability,
        penalty
    )

    no_improvement_count = 0

    iterations_used = 0

    # -------------------------
    # Hill climbing
    # -------------------------

    for i in range(max_iterations):

        iterations_used = i + 1

        # Tạo neighbor
        neighbor_key = mutate_key(current_key)

        # Decrypt bằng neighbor
        neighbor_plaintext = decrypt(
            ciphertext,
            neighbor_key
        )

        # Tính score
        neighbor_score = score_text(
            neighbor_plaintext,
            log_probability,
            penalty
        )
        print("Initial score:", current_score)

        # -------------------------
        # Nếu tốt hơn -> accept
        # -------------------------

        if neighbor_score > current_score:

            current_key = neighbor_key
            current_score = neighbor_score

            no_improvement_count = 0

        else:

            no_improvement_count += 1

        # -------------------------
        # Early stopping
        # -------------------------

        if no_improvement_count >= MAX_NO_IMPROVEMENT:
            break

    return current_key, current_score, iterations_used


# ============================================================
# 8. TEST SCORING
# ============================================================

def test_scoring(log_probability, penalty):

    english = (
        "the government announced that the new system "
        "will be available for all users"
    )

    random_text = (
        "xqz jkwpf zmxqv bcnmz qwx zplmnf qzx "
        "vjkx qwpz mnxq"
    )

    english_score = score_text(
        english,
        log_probability,
        penalty
    )

    random_score = score_text(
        random_text,
        log_probability,
        penalty
    )

    print("\n=== Scoring Test ===")

    print("English score:", english_score)
    print("Random score :", random_score)

    if english_score > random_score:
        print("Result: Scoring model works correctly.")
    else:
        print("Result: Warning - scoring model may have a problem.")


# ============================================================
# 9. MAIN
# ============================================================

def main():

    print("=== Monoalphabetic Substitution Cipher Solver ===")

    # ========================================================
    # LOAD TRIGRAM DATA
    # ========================================================

    print("\nLoading English trigram data...")

    log_probability, penalty = load_trigram_data(TRIGRAM_FILE)

    print(
        "Number of trigrams:",
        len(log_probability)
    )

    print(
        "Unknown trigram penalty:",
        penalty
    )

    # ========================================================
    # TEST SCORING MODEL
    # ========================================================

    test_scoring(
        log_probability,
        penalty
    )

    # ========================================================
    # INPUT
    # ========================================================

    print("\n=== Input ===")

    print("1. Enter ciphertext")
    print("2. Read ciphertext from file")

    choice = input("Choose: ")

    if choice == "1":

        ciphertext = input(
            "Enter ciphertext: "
        )

    elif choice == "2":

        with open(
            CIPHERTEXT_FILE,
            "r"
        ) as f:

            ciphertext = f.read()

    else:

        print("Invalid choice.")

        return

    # ========================================================
    # NORMALIZE FOR SEARCH
    # ========================================================

    normalized_ciphertext = normalize_text(
        ciphertext
    )

    print(
        "\nCiphertext length:",
        len(normalized_ciphertext)
    )

    # ========================================================
    # RANDOM RESTART HILL CLIMBING
    # ========================================================

    print(
        "\n=== Random-Restart Hill Climbing ==="
    )

    best_overall_key = None

    best_overall_score = float("-inf")

    best_restart = 0

    # --------------------------------------------------------
    # Restart nhiều lần
    # --------------------------------------------------------

    for run in range(NUM_RESTARTS):

        key, score, iterations = solve_cipher(
            normalized_ciphertext,
            log_probability,
            penalty
        )

        print(
            f"Restart {run + 1:02}/{NUM_RESTARTS} "
            f"| Score: {score:.6f} "
            f"| Iterations: {iterations}"
        )

        # ----------------------------------------------------
        # Nếu đây là kết quả tốt nhất
        # ----------------------------------------------------

        if score > best_overall_score:

            best_overall_score = score

            best_overall_key = key

            best_restart = run + 1

    # ========================================================
    # FINAL DECRYPTION
    # ========================================================

    # Quan trọng:
    #
    # Dùng ciphertext GỐC thay vì normalized_ciphertext
    # để giữ lại khoảng trắng, dấu câu và newline.

    plaintext = decrypt(
        ciphertext,
        best_overall_key
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print("\n")
    print("=" * 60)

    print("BEST RESULT")

    print("=" * 60)

    print(
        "\nBest restart:",
        best_restart
    )

    print(
        "Best score:",
        best_overall_score
    )

    print("\nKey:")

    print(
        "Plain : abcdefghijklmnopqrstuvwxyz"
    )

    print(
        "Cipher:",
        best_overall_key
    )

    print("\nDecrypted Text:\n")

    print(plaintext)

    print("\n" + "=" * 60)

    # 2. Ghi kết quả giải mã ra file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(plaintext)
    print(f"Đã ghi kết quả thành công vào file {OUTPUT_FILE}!")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()