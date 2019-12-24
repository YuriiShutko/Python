import string


def main():
    input_file = input('Input file name: ')
    output_file = input('Output file name: ')
    mode = input('1 - encrypt\n2 - decrypt\nMake your choice: ')
    key = check_input(mode)
    with open(input_file, 'r') as r:
        input_str = r.read()
    with open(output_file, 'w') as w:
        w.write(encrypt_string(input_str, key))


def check_input(mode):
    key = check_input(int(input('Input key: ')))
    if mode == '2':
        key = -key
    elif mode != '1':
        print("Illegal parameter...")
        exit()
    return key


def encrypt_string(input_string, key):
    a = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    symbols = a + " " + a.upper() + string.ascii_letters + string.digits + string.punctuation
    encrypted_string, length_symbols = "", len(symbols)
    for input_char in input_string:
        found_char_index = symbols.find(input_char)
        if found_char_index == -1:
            encrypted_string += input_char
        else:
            new_index = (found_char_index + key) % length_symbols
            encrypted_string += symbols[new_index]

    return encrypted_string


main()
