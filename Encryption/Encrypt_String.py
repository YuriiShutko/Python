import string


def main():
    input_file = input('Input file name: ')
    output_file = input('Output file name: ')

    with open(input_file, 'r') as r:
        input_str = r.read()
    with open(output_file, 'w') as w:
        w.write(encrypt_string(input_str, int(input('Input number shift: ')),
                               input('1 - encrypt\n2 - decrypt\nMake your choice: ')))
        w.flush()


def encrypt_string(input_string, number_shift, mode):
    if mode == '1':
        number_shift = number_shift
    elif mode == '2':
        number_shift = -number_shift
    else:
        print("Illegal parameter...")
        exit()

    a = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    symbols = a + " " + a.upper() + string.ascii_letters + string.digits + string.punctuation
    encrypted_string, length_symbols = "", len(symbols)
    for input_char in input_string:
        found_char_index = symbols.find(input_char)
        if found_char_index == -1:
            encrypted_string += input_char
        else:
            new_index = (found_char_index + number_shift) % length_symbols
            encrypted_string += symbols[new_index]

    return encrypted_string


main()
