from math import sqrt
from nostril import nonsense

cipher = input("Enter ciphertext: ")
cipher = cipher.upper()
temp = ""
plain = list()
occ_dict = {
    "E": 12.31,
    "T": 9.59,
    "A": 8.05,
    "O": 7.94,
    "N": 7.19,
    "I": 7.18,
    "S": 6.59,
    "R": 6.03,
    "H": 5.14,
    "L": 4.03,
    "D": 3.65,
    "C": 3.2,
    "U": 3.1,
    "P": 2.29,
    "F": 2.28,
    "M": 2.25,
    "W": 2.03,
    "Y": 1.88,
    "B": 1.62,
    "G": 1.61,
    "V": 0.93,
    "K": 0.52,
    "X": 0.2,
    "Q": 0.2,
    "J": 0.1,
    "Z": 0.09,
}
occur = {}
dist = {}

for key in range(0, 26):
    for char_old in cipher:
        if ord(char_old) < 65 or ord(char_old) > 90:
            temp += char_old
            continue
        if ord(char_old) + key <= 90:
            char_new = chr(ord(char_old) + key)
        else:
            char_new = chr(ord(char_old) + key - 26)
        if char_new in occur:
            occur[char_new] += 1
        else:
            occur[char_new] = 1
        temp += char_new
    plain.append(temp)
    diff = 0
    for o in sorted(occur.items(), key=lambda x: x[1], reverse=True):
        diff += (o[1] - occ_dict[o[0]])**2
    dist[key] = sqrt(diff)
    temp = ""
    occur = {}

for key in sorted(dist.items(), key=lambda x: x[1]):
    print(
        "\033[94m" + "Key:",
        key[0],
        "\033[97m" + "-",
        "\033[95m" + "Plaintext:",
        "\033[97m" + plain[key[0]],
        "\033[97m" + "-",
        "\033[96m" + "Mismatch:",
        dist[key[0]],
        "\033[97m" + "-",
        ("\033[91m" + "Meaningful: False"
         if nonsense(plain[key[0]]) else "\033[92m" + "Meaningful: True"),
    )
