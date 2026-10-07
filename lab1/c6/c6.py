import math


# ============================================================
# CONFIG
# ============================================================

CIPHERTEXT_FILE = "c6.txt"
TRIGRAM_FILE = "../english_trigrams.txt"
OUTPUT_FILE = "c6_output.txt"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228,
    2.015, 6.094, 6.966, 0.153, 0.772, 4.025,
    2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
    6.327, 9.056, 2.758, 0.978, 2.360, 0.150,
    1.974, 0.074
]


# ============================================================
# TEXT PROCESSING
# ============================================================

def normalize_text(text):
    return ''.join(
        char for char in text.lower()
        if 'a' <= char <= 'z'
    )


# ============================================================
# INDEX OF COINCIDENCE
# ============================================================

def index_of_coincidence(text):
    text = normalize_text(text)
    n = len(text)

    if n < 2:
        return 0.0

    frequencies = [0] * 26

    for char in text:
        frequencies[ord(char) - ord('a')] += 1

    numerator = sum(
        freq * (freq - 1)
        for freq in frequencies
    )

    return numerator / (n * (n - 1))


# ============================================================
# SPLIT INTO GROUPS
# ============================================================

def split_into_groups(ciphertext, key_length):
    text = normalize_text(ciphertext)

    return [
        text[i::key_length]
        for i in range(key_length)
    ]


# ============================================================
# ESTIMATE KEY LENGTH
# ============================================================

def estimate_key_lengths(ciphertext, max_key_length=20):
    results = []

    for key_length in range(1, max_key_length + 1):

        groups = split_into_groups(
            ciphertext,
            key_length
        )

        average_ic = sum(
            index_of_coincidence(group)
            for group in groups
        ) / len(groups)

        results.append(
            (key_length, average_ic)
        )

    # IC càng cao càng đáng xem xét
    results.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return results


# ============================================================
# CAESAR ANALYSIS
# ============================================================

def caesar_decrypt(text, shift):
    result = ""

    for char in text:
        c = ord(char) - ord('a')
        p = (c - shift) % 26

        result += chr(
            p + ord('a')
        )

    return result


def chi_squared(text):
    text = normalize_text(text)
    n = len(text)

    if n == 0:
        return float("inf")

    observed = [0] * 26

    for char in text:
        observed[ord(char) - ord('a')] += 1

    score = 0.0

    for i in range(26):

        expected = (
            ENGLISH_FREQ[i]
            / 100
            * n
        )

        score += (
            (observed[i] - expected) ** 2
            / expected
        )

    return score


def find_caesar_shift(group):
    best_shift = 0
    best_score = float("inf")

    # Thử toàn bộ Caesar shift 0-25
    for shift in range(26):

        decrypted = caesar_decrypt(
            group,
            shift
        )

        score = chi_squared(decrypted)

        # Chi-squared càng nhỏ càng tốt
        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift, best_score


# ============================================================
# RECOVER VIGENERE KEY
# ============================================================

def recover_key(ciphertext, key_length):
    groups = split_into_groups(
        ciphertext,
        key_length
    )

    key = ""
    shift_scores = []

    for group in groups:

        shift, score = find_caesar_shift(group)

        key += chr(
            shift + ord('a')
        )

        shift_scores.append(score)

    return key, shift_scores


# ============================================================
# VIGENERE DECRYPT
# ============================================================

def vigenere_decrypt(ciphertext, key):
    result = ""
    key_index = 0

    for char in ciphertext:

        if 'a' <= char.lower() <= 'z':

            c = (
                ord(char.lower())
                - ord('a')
            )

            k = (
                ord(key[key_index % len(key)])
                - ord('a')
            )

            p = (c - k) % 26

            plain_char = chr(
                p + ord('a')
            )

            if char.isupper():
                plain_char = plain_char.upper()

            result += plain_char

            key_index += 1

        else:
            # Giữ nguyên space và punctuation
            result += char

    return result


# ============================================================
# TRIGRAM LANGUAGE MODEL
# ============================================================

def load_trigram_data(filename):
    counts = {}

    with open(filename, "r") as file:

        for line in file:
            parts = line.split()

            if len(parts) != 2:
                continue

            trigram = parts[0].lower()
            count = int(parts[1])

            counts[trigram] = count

    total = sum(counts.values())

    log_probability = {
        trigram: math.log10(count / total)
        for trigram, count in counts.items()
    }

    penalty = math.log10(
        0.1 / total
    )

    return log_probability, penalty


def trigram_score(
    text,
    log_probability,
    penalty
):
    text = normalize_text(text)

    num_trigrams = len(text) - 2

    if num_trigrams <= 0:
        return penalty

    score = 0.0

    for i in range(num_trigrams):

        trigram = text[i:i + 3]

        score += log_probability.get(
            trigram,
            penalty
        )

    return score / num_trigrams


# ============================================================
# VIGENERE SOLVER
# ============================================================

def solve_vigenere(
    ciphertext,
    log_probability,
    penalty,
    max_key_length=20,
    num_candidates=5
):
    # 1. Ước lượng key length bằng IC
    key_length_results = estimate_key_lengths(
        ciphertext,
        max_key_length
    )

    # 2. Lấy top candidate
    candidates = key_length_results[
        :num_candidates
    ]

    best_result = None
    analysis_results = []

    # 3. Thử từng key length
    for key_length, average_ic in candidates:

        # Tìm key bằng Chi-squared
        key, shift_scores = recover_key(
            ciphertext,
            key_length
        )

        # Giải mã
        plaintext = vigenere_decrypt(
            ciphertext,
            key
        )

        # Đánh giá plaintext bằng trigram
        score = trigram_score(
            plaintext,
            log_probability,
            penalty
        )

        result = {
            "key_length": key_length,
            "average_ic": average_ic,
            "key": key,
            "trigram_score": score,
            "shift_scores": shift_scores,
            "plaintext": plaintext
        }

        analysis_results.append(result)

        # Trigram score càng cao càng tốt
        if (
            best_result is None
            or score > best_result["trigram_score"]
        ):
            best_result = result

    return best_result, analysis_results


# ============================================================
# INPUT
# ============================================================

def read_ciphertext():
    print("1. Enter ciphertext")
    print("2. Read ciphertext from file")

    choice = input("\nChoose: ").strip()

    if choice == "1":
        print("\nEnter ciphertext:")
        return input()

    if choice == "2":
        with open(
            CIPHERTEXT_FILE,
            "r"
        ) as file:
            return file.read()

    raise ValueError("Invalid choice.")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("VIGENERE CIPHER BREAKER")
    print("=" * 60)

    # Load trigram model
    try:
        log_probability, penalty = load_trigram_data(
            TRIGRAM_FILE
        )

    except FileNotFoundError:
        print(
            f"Error: Cannot find {TRIGRAM_FILE}"
        )
        return

    # Read ciphertext
    try:
        ciphertext = read_ciphertext()

    except (ValueError, FileNotFoundError) as error:
        print("Error:", error)
        return

    normalized = normalize_text(ciphertext)

    if len(normalized) < 3:
        print("Ciphertext is too short.")
        return

    print(
        "\nCiphertext length:",
        len(normalized)
    )

    # Solve
    best_result, analysis_results = solve_vigenere(
        ciphertext,
        log_probability,
        penalty,
        max_key_length=20,
        num_candidates=5
    )

    # --------------------------------------------------------
    # Candidate results
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CANDIDATE RESULTS")
    print("=" * 60)

    for result in analysis_results:

        print(
            f"\nKey length   : "
            f"{result['key_length']}"
        )

        print(
            f"Average IC   : "
            f"{result['average_ic']:.6f}"
        )

        print(
            f"Recovered key: "
            f"{result['key']}"
        )

        print(
            f"Trigram score: "
            f"{result['trigram_score']:.6f}"
        )

    # --------------------------------------------------------
    # Best result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("BEST RESULT")
    print("=" * 60)

    print(
        "Key length:",
        best_result["key_length"]
    )

    print(
        "Key:",
        best_result["key"]
    )

    print(
        "Average IC:",
        f"{best_result['average_ic']:.6f}"
    )

    print(
        "Trigram score:",
        f"{best_result['trigram_score']:.6f}"
    )

    print("\nPlaintext:\n")

    print(
        best_result["plaintext"]
    )

    # 2. Ghi kết quả giải mã ra file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(best_result["plaintext"])
    print(f"\nĐã ghi kết quả thành công vào file {OUTPUT_FILE}!")




if __name__ == "__main__":
    main()