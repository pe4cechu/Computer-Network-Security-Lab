global new_word

def filter_text(text):
    new_text = ""
    for i in text:
        if ord(i) < 65 or ord(i) > 90:
            continue
        else:
            new_text = new_text + i
    return new_text

def diagraph(text):
    diag = []
    group = 0
    for i in range(2, len(text), 2):
        diag.append(text[group:i])

        group = i
    diag.append(text[group:])
    return diag

def filler_letter(text):
    global new_word
    k = len(text)
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i+1]:
                new_word = text[0:i+1] + str('X') + text[i+1:]
                new_word = filler_letter(new_word)
                break
            else:
                new_word = text
    else:
        for i in range(0, k-1, 2):
            if text[i] == text[i+1]:
                new_word = text[0:i+1] + str('X') + text[i+1:]
                new_word = filler_letter(new_word)
                break
            else:
                new_word = text
    return new_word


alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def generate_key_table(word, alphabet):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)

    comp_elements = []
    for i in key_letters:
        if i not in comp_elements:
            comp_elements.append(i)
    for i in alphabet:
        if i not in comp_elements:
            comp_elements.append(i)

    matrix = []
    while comp_elements:
        matrix.append(comp_elements[:5])
        comp_elements = comp_elements[5:]

    return matrix


def search(mat, element):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == element:
                return i, j


def encrypt_row_rule(matr, e1r, e1c, e2r, e2c):
    if e1c == 4:
        char1 = matr[e1r][0]
    else:
        char1 = matr[e1r][e1c+1]

    if e2c == 4:
        char2 = matr[e2r][0]
    else:
        char2 = matr[e2r][e2c+1]

    return char1, char2


def encrypt_column_rule(matr, e1r, e1c, e2r, e2c):
    if e1r == 4:
        char1 = matr[0][e1c]
    else:
        char1 = matr[e1r+1][e1c]

    if e2r == 4:
        char2 = matr[0][e2c]
    else:
        char2 = matr[e2r+1][e2c]

    return char1, char2


def encrypt_rectangle_rule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][e2c]
    char2 = matr[e2r][e1c]
    return char1, char2


def encrypt_by_playfair_cipher(matrix, plain_list):
    cipher_text = []
    for i in range(0, len(plain_list)):
        ele1_x, ele1_y = search(matrix, plain_list[i][0])
        ele2_x, ele2_y = search(matrix, plain_list[i][1])

        if ele1_x == ele2_x:
            c1, c2 = encrypt_row_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            # Get 2 letter cipherText
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_column_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_rectangle_rule(
                matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        cipher = c1 + c2
        cipher_text.append(cipher)
    return cipher_text


plain = input("Enter plaintext: ")

plain = filter_text(plain.upper())
plain_list = diagraph(filler_letter(plain))
if len(plain_list[-1]) != 2:
    plain_list[-1] = plain_list[-1] + 'X'

key = input("Enter key: ")

matrix = generate_key_table(key.upper(), alphabet)

cipher_list = encrypt_by_playfair_cipher(matrix, plain_list)

cipher = ""
for i in cipher_list:
    cipher += i
print('\033[93m' + "Ciphertext:",'\033[97m' + cipher)