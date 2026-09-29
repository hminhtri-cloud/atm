text = input("Đoạn văn: ")
common_words = ["the", "and", "to", "of", "a", "in", "that", "is", "it", "for"]
best_k = 0
best_text = ""
best_count = 0
for k in range(1, 26):
    re = ""
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
    count = 0
    for word in common_words:
        count += re.lower().count(word)
    if count > best_count:
        best_count = count
        best_k = k
        best_text = re

print(f"Khóa: {best_k}")
print(f"Đoạn văn đã giải mã: {best_text}")
