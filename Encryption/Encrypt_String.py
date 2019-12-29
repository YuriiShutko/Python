import string


def main():
    try:
        input_file_name = input('Input file name: ')
        output_file_name = input('Output file name: ')
        mode = int(input('1 - encrypt\n2 - decrypt\nMake your choice: '))
        key = get_key(mode, int(input('Input key: ')))
        original_str = read_from_file(input_file_name)
        modified_str = encrypt_string(original_str, key)
        write_to_file(output_file_name, modified_str)
    except FileNotFoundError:
        print('There is no such file!')
    except ValueError:
        print('Illegal key or mode format')


def read_from_file(input_file_name):
    with open(input_file_name, 'r') as r:
        input_str = r.read()
    return input_str


def write_to_file(output_file_name, out_str):
    with open(output_file_name, 'w') as w:
        w.write(out_str)


def get_key(mode, key_of_encryption):
    if mode == 2:
        key_of_encryption = -key_of_encryption
    elif mode != 1:
        raise ValueError('Illegal mode parameter...')
    return key_of_encryption


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
