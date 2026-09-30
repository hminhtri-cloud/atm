def create_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper().replace("J", "I")
    text = ""
    for char in key:
        if char.isalpha() and char not in text:
            text += char
    for char in alphabet:
        if char not in text:
            text += char
    matrix = []

    for i in range(0, 25, 5):
        matrix.append(text[i:i+5])

    return matrix
def print_matrix(matrix):
    print("\nMa trận Playfair:")
    for row in matrix:
        print(" ".join(row))
    print()
def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = "".join(char for char in text if char.isalpha())
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 >= len(text):
            result += a + "X"
            i += 1
        else:
            b = text[i + 1]
            if a == b:
                result += a + "X"
                i += 1
            else:
                result += a + b
                i += 2
    return result
def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
def encrypt(text, matrix):
    text = prepare_text(text)
    result = ""
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1 + 1) % 5]
            result += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            result += matrix[(row1 + 1) % 5][col1]
            result += matrix[(row2 + 1) % 5][col2]
        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]
    return result
def decrypt(text, matrix):
    text = text.upper().replace("J", "I")
    result = ""
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1 - 1) % 5]
            result += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            result += matrix[(row1 - 1) % 5][col1]
            result += matrix[(row2 - 1) % 5][col2]
        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]
    return result
key = input("Nhập khóa: ")
matrix = create_matrix(key)
print_matrix(matrix)
choice = int(input("1. Mã hóa\n2. Giải mã\nChọn: "))
text = input("Nhập văn bản: ")
if choice == 1:
    result = encrypt(text, matrix)
    print("Ciphertext:", result)
elif choice == 2:
    result = decrypt(text, matrix)
    print("Plaintext:", result)
else:
    print("Vui lòng chọn 1 hoặc 2.")