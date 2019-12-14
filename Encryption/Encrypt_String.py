import string


def get_comparable_string():
    a = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    symbols = a + a.upper() + string.ascii_letters + string.digits
    return symbols


def get_input_string():
    input_string = input("Input your string: ")
    return input_string


def encrypt_string(number_shift):
    encrypted_string = ""
    trigger = False
    last_index_compstr = len(get_comparable_string()) - 1
    for input_sym in get_input_string():
        if input_sym == " ":
            encrypted_string += " "
        for symbol in get_comparable_string():
            if input_sym == symbol:
                current_ind_compstr = get_comparable_string().index(symbol)
                if current_ind_compstr + number_shift <= last_index_compstr:
                    encrypted_string += get_comparable_string()[current_ind_compstr + number_shift]
                else:
                    difference = current_ind_compstr + number_shift - len(get_comparable_string())
                    if difference >= 0:
                        if 0 + difference <= last_index_compstr:
                            encrypted_string += get_comparable_string()[0 + difference]
                        else:
                            print("Слишком большой сдвиг")
                            trigger = True
        if trigger:
            break

    return encrypted_string
