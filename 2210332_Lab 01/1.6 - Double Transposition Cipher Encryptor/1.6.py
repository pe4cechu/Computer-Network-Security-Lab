def replace_string(string):
    for char in string:
        if ord(char) < 65 or ord(char) > 90:
            string = string.replace(char, '')
    return string

def count_rows(key, plain):
    if len(plain) % len(key):
        return len(plain) // len(key) + 1
    else:
        return len(plain) // len(key)

def print_matrix(key, matrix, color):
    color_code = '\033[' + str(color) + 'm'
    for char in key:
        print(color_code + char, end=' ')
    print()
    for i in range(len(key)):
        print(color_code + "-", end=' ')
    for i in range(len(matrix)):
        print()
        for j in range(len(matrix[i])):
            print(color_code + matrix[i][j], end=' ')
    print('\n')

def create_matrix(key, plain):
    matrix = list()
    counter = 0
    for i in range(count_rows(key, plain)):
        temp = []
        for j in range(len(key)):
            if counter == len(plain):
                break
            temp.append(plain[counter])
            counter += 1
        matrix.append(temp)
    return matrix

def sort_key(key, color):
    color_code = '\033[' + str(color) + 'm'
    order = [-1] * len(key)
    occur = list()
    dup = {}
    counter = 0
    for char in key:
        if char in occur:
            dup[char] += 1
        else:
            dup[char] = 0
        occur.append(char)
        num = sorted(key).index(char) + dup[char]
        order[num] = counter
        counter += 1
        print(color_code + str(num + 1), end=' ')
    print()
    return order

def transpose_encryption(matrix, key, row, order, plain):
    string = ""
    for j in range(len(key)):
        for i in range(row):
            if i * len(key) + order[j] >= len(plain):
                break
            string += matrix[i][order[j]]
    return string

plain1 = input("Enter plaintext: ")
key1 = input("Enter 1st key: ")
key2 = input("Enter 2nd key: ")
plain1 = replace_string(plain1.upper())
key1 = replace_string(key1)
row1 = count_rows(key1, plain1)
matrix1 = create_matrix(key1, plain1)
print ('\033[97m' + "First transposition matrix:",)
order1 = sort_key(key1, 95)
print_matrix(key1, matrix1, 95)

key2 = replace_string(key2)
row2 = count_rows(key2, plain1)
plain2 = transpose_encryption(matrix1, key1, row1, order1, plain1)
matrix2 = create_matrix(key2, plain2)
print ('\033[97m' + "Second transposition matrix:",)
order2 = sort_key(key2, 94)
print_matrix(key2, matrix2, 94)

cipher = transpose_encryption(matrix2, key2, row2, order2, plain2)

print ('\033[97m' + "Ciphertext:",)
for i in range(0, len(cipher), 5):
    print('\033[93m' + cipher[i:i+5], end=' ')

