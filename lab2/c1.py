def F(right, subkey):
    return (right ^ subkey) & 0x0F
def feistel_round(L_in, R_in, subkey):
# TODO: Triển khai LE_i = RE_{i-1} và RE_i = LE_{i-1} XOR F(...)
    def track_avalanche(msg, key):
# L, R = (msg >> 4) & 0x0F, msg & 0x0F
# subkeys = [key & 0x0F, (key >> 4) & 0x0F, (key + 1) & 0x0F, (key + 2) & 0x0F]
    print(f"Khởi tạo: L={format(L, f’0{4}b’)}, R={format(R, f’0{4}b’)}")
for i in range(4):
L, R = feistel_round(L, R, subkeys[i])
print(f"Vòng {i+1}: L={format(L, f’0{4}b’)}, R={format(R, f’0{4}b’)}")
return (L << 4) | R