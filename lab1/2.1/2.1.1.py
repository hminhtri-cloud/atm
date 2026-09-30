k = int(input("Nhập khóa: "))
n = int(input("1. Mã hóa\n2. Giải mã\nChọn: "))
text = input("Đoạn văn: ")
re = ""
if n == 1:
    for char in text:
        if char.isupper():
            x = ord(char) - ord('A')
            x = (x + k) % 26
            re += chr(x + ord('A'))
        elif char.islower():
            x = ord(char) - ord('a')
            x = (x + k) % 26
            re += chr(x + ord('a'))
        else:
            re += char

elif n == 2:
    for char in text:
        if char.isupper():
            x = ord(char) - ord('A')
            x = (x - k) % 26
            re += chr(x + ord('A'))
        elif char.islower():
            x = ord(char) - ord('a')
            x = (x - k) % 26
            re += chr(x + ord('a'))
        else:
            re += char
else:
    print("Vui lòng chọn 1 hoặc 2.")
print("Kết quả:", re)