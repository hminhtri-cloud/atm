from Crypto.Cipher import AES
from Crypto.Util import Counter

def print_blocks(label, ciphertext):
    print(f"{label}: {ciphertext.hex()}")
    for index in range(0, len(ciphertext), AES.block_size):
        print(f"  block {index // AES.block_size + 1}: {ciphertext[index:index + AES.block_size].hex()}")

# 1. AES-ECB
def encrypt_ecb(plaintext, key):
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    return cipher_ecb.encrypt(plaintext)

# 2. AES-CBC
def encrypt_cbc(plaintext, key, iv):
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
    return cipher_cbc.encrypt(plaintext)

# 3. AES-CFB
def encrypt_cfb(plaintext, key, iv):
    cipher_cfb = AES.new(key, AES.MODE_CFB, iv)
    return cipher_cfb.encrypt(plaintext)

# 3. AES-OFB
def encrypt_ofb(plaintext, key, iv):
    cipher_ofb = AES.new(key, AES.MODE_OFB, iv)
    return cipher_ofb.encrypt(plaintext)

# 3. AES-CTR
def encrypt_ctr(plaintext, key, iv):
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher_ctr = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher_ctr.encrypt(plaintext)

def main():

    KEY = b"1234567890123456"
    IV = b"6543210987654321"
    PLAINTEXT = b"UIT_LAB_UIT_LAB_UIT_LAB_UIT_LAB_"

    if len(PLAINTEXT) % AES.block_size:
        raise ValueError("Plaintext must contain complete AES blocks")

    ct_ecb = encrypt_ecb(PLAINTEXT, KEY)
    ct_cbc = encrypt_cbc(PLAINTEXT, KEY, IV)
    ct_cfb = encrypt_cfb(PLAINTEXT, KEY, IV)
    ct_ofb = encrypt_ofb(PLAINTEXT, KEY, IV)
    ct_ctr = encrypt_ctr(PLAINTEXT, KEY, IV)

    print_blocks("ECB", ct_ecb)
    print_blocks("CBC", ct_cbc)
    print_blocks("CFB", ct_cfb)
    print_blocks("ofb", ct_ofb)
    print_blocks("ctr", ct_ctr)

    ecb_blocks = [ct_ecb[i:i + 16] for i in range(0, len(ct_ecb), 16)]
    cbc_blocks = [ct_cbc[i:i + 16] for i in range(0, len(ct_cbc), 16)]
    cfb_blocks = [ct_cfb[i:i + 16] for i in range(0, len(ct_cfb), 16)]
    ofb_blocks = [ct_ofb[i:i + 16] for i in range(0, len(ct_ofb), 16)]
    ctr_blocks = [ct_ctr[i:i + 16] for i in range(0, len(ct_ctr), 16)]

    print(f"ECB blocks giong nhau: {ecb_blocks[0] == ecb_blocks[1]}")
    print(f"CBC blocks giong nhau: {cbc_blocks[0] == cbc_blocks[1]}")
    print(f"CBC blocks giong nhau: {cfb_blocks[0] == cfb_blocks[1]}")
    print(f"OFB blocks giong nhau: {ofb_blocks[0] == ofb_blocks[1]}")
    print(f"CTR blocks giong nhau: {ctr_blocks[0] == ctr_blocks[1]}")


if __name__ == "__main__":
    main()
