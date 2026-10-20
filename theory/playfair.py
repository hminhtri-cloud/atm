
# Tao ma tran khoa Playfair
def create_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper().replace("J", "I")

    key = ''.join(
        char for char in key if char in alphabet
    )

    sequence = ""

    for char in key + alphabet:
        if char not in sequence:
            sequence += char

    matrix = [
        list(sequence[i:i + 5])
        for i in range(0, 25, 5)
    ]

    return matrix


# Tim vi tri ky tu trong ma tran
def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

    raise ValueError("Ky tu khong hop le!")


# Chuan hoa van ban
def normalize(text):
    return ''.join(
        char for char in text.upper().replace("J", "I")
        if 'A' <= char <= 'Z'
    )


# Chia ban ro thanh cac cap ky tu
def prepare_text(text):
    text = normalize(text)
    result = ""
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 >= len(text):
            b = 'X' if a != 'X' else 'Q'
            i += 1

        elif a == text[i + 1]:
            b = 'X' if a != 'X' else 'Q'
            i += 1

        else:
            b = text[i + 1]
            i += 2

        result += a + b

    return result


# Xu ly ma hoa va giai ma mot cap
def process_pair(a, b, matrix, decrypt=False):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    shift = -1 if decrypt else 1

    if r1 == r2:
        c1 = (c1 + shift) % 5
        c2 = (c2 + shift) % 5

    elif c1 == c2:
        r1 = (r1 + shift) % 5
        r2 = (r2 + shift) % 5

    else:
        c1, c2 = c2, c1

    return matrix[r1][c1] + matrix[r2][c2]


# Ma hoa Playfair
def playfair_encrypt(text, key):
    matrix = create_matrix(key)
    text = prepare_text(text)
    result = ""

    for i in range(0, len(text), 2):
        result += process_pair(
            text[i], text[i + 1], matrix
        )

    return result


# Giai ma Playfair
def playfair_decrypt(text, key):
    matrix = create_matrix(key)
    text = normalize(text)

    if len(text) % 2 != 0:
        raise ValueError("Ban ma phai co do dai chan!")

    result = ""

    for i in range(0, len(text), 2):
        result += process_pair(
            text[i], text[i + 1], matrix, True
        )

    return result


# Hien thi ma tran khoa
def show_matrix(matrix):
    print("\nMa tran khoa Playfair:")

    for row in matrix:
        print(" ".join(row))


# Chuong trinh chinh
while True:
    print("\n===== PLAYFAIR CIPHER =====")
    print("1. Ma hoa")
    print("2. Giai ma")
    print("0. Thoat")

    choice = input("Chon chuc nang: ")

    if choice == "0":
        break

    if choice not in ("1", "2"):
        print("Lua chon khong hop le!")
        continue

    key = input("Nhap khoa: ")
    text = input("Nhap van ban: ")

    matrix = create_matrix(key)
    show_matrix(matrix)

    try:
        if choice == "1":
            print(
                "Ban ma:",
                playfair_encrypt(text, key)
            )

        else:
            print(
                "Ban ro:",
                playfair_decrypt(text, key)
            )

    except ValueError as e:
        print("Loi:", e)
