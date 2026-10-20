
# Khoi tao bo bai 54 la
def create_deck():
    return list(range(1, 55))


# Di chuyen Joker xuong mot vi tri
def move_joker(deck, joker):
    index = deck.index(joker)
    deck.pop(index)

    if index == len(deck):
        deck.insert(1, joker)
    else:
        deck.insert(index + 1, joker)


# Cat bo bai tai hai Joker
def triple_cut(deck):
    a = deck.index(53)
    b = deck.index(54)

    first, second = sorted([a, b])

    deck[:] = (
        deck[second + 1:]
        + deck[first:second + 1]
        + deck[:first]
    )


# Count Cut
def count_cut(deck):
    count = min(deck[-1], 53)

    deck[:] = (
        deck[count:-1]
        + deck[:count]
        + deck[-1:]
    )


# Tao mot gia tri khoa
def generate_key_value(deck):
    while True:
        # Buoc 1: Joker A xuong 1 vi tri
        move_joker(deck, 53)

        # Buoc 2: Joker B xuong 2 vi tri
        move_joker(deck, 54)
        move_joker(deck, 54)

        # Buoc 3: Triple Cut
        triple_cut(deck)

        # Buoc 4: Count Cut
        count_cut(deck)

        # Buoc 5: Tim la bai dau ra
        count = min(deck[0], 53)
        value = deck[count]

        # Bo qua neu la Joker
        if value > 52:
            continue

        # Chuyen ve gia tri 1-26
        return (value - 1) % 26 + 1


# Tao chuoi khoa
def generate_keystream(deck, length):
    return [
        generate_key_value(deck)
        for _ in range(length)
    ]


# Chuan hoa van ban
def prepare_text(text):
    return ''.join(
        c for c in text.upper()
        if 'A' <= c <= 'Z'
    )


# Ma hoa Solitaire
def solitaire_encrypt(text, deck):
    text = prepare_text(text)
    keys = generate_keystream(deck, len(text))
    result = ""

    for char, key in zip(text, keys):
        p = ord(char) - 64
        c = (p + key - 1) % 26 + 1
        result += chr(c + 64)

    return result


# Giai ma Solitaire
def solitaire_decrypt(text, deck):
    text = prepare_text(text)
    keys = generate_keystream(deck, len(text))
    result = ""

    for char, key in zip(text, keys):
        c = ord(char) - 64
        p = (c - key - 1) % 26 + 1
        result += chr(p + 64)

    return result


# Chuong trinh chinh
while True:
    print("\n===== SOLITAIRE CIPHER =====")
    print("1. Ma hoa")
    print("2. Giai ma")
    print("0. Thoat")

    choice = input("Chon chuc nang: ")

    if choice == "0":
        break

    if choice not in ("1", "2"):
        print("Lua chon khong hop le!")
        continue

    if choice not in ("1", "2"):
        continue

    # Hai ben phai dung cung bo bai ban dau
    deck = create_deck()
    text = input("Nhap van ban: ")

    if choice == "1":
        print(
            "Ban ma:",
            solitaire_encrypt(text, deck)
        )
    else:
        print(
            "Ban ro:",
            solitaire_decrypt(text, deck)
        )
