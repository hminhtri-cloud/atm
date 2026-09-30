key = input("Nhập khóa: ").upper()
n = int(input("1. Mã hóa\n2. Giải mã\nChọn: "))
text = input("Đoạn văn: ")
result = ""
key_index = 0
for char in text:
    if char.isalpha():
        k = ord(key[key_index % len(key)]) - ord('A')
        if char.isupper():
            x = ord(char) - ord('A')
            if n == 1:
                x = (x + k) % 26
            elif n == 2:
                x = (x - k) % 26
            result += chr(x + ord('A'))
        elif char.islower():
            x = ord(char) - ord('a')
            if n == 1:
                x = (x + k) % 26
            elif n == 2:
                x = (x - k) % 26
            result += chr(x + ord('a'))
        key_index += 1
    else:
        result += char
if n == 1 or n == 2:
    print("Kết quả:", result)
else:
    print("Vui lòng chọn 1 hoặc 2.")