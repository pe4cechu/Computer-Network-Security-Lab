pc1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

pc2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

plaintext = int(input("Enter plaintext: "), 16)
key = int(input("Enter key: "), 16)

key_64 = f"{key:064b}"
key_56 = "".join(key_64[pc1[i] - 1] for i in range(56))

c = key_56[:28]
d = key_56[28:]

c1 = c[1:] + c[0]
d1 = d[1:] + d[0]

k1 = "".join((c1 + d1)[pc2[i] - 1] for i in range(48))

print(f"\033[95mKey K1: \033[97m{hex(int(k1, 2))[2:].upper()}")
