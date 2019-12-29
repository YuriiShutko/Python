from getpass import getpass
from Encrypt_String import read_from_file, write_to_file, encrypt_string, get_key
import json


def ask_credentials():
    """
    This function ask user to enter his credentials
    :return: Returns a tuple with the following (username, user_pass)
    """
    username = input('Login: ')
    user_pass = getpass(prompt='Password: ')
    return username, user_pass


def create_new_user():
    """
    This function creates a new user and add him to the users dictionary
    """
    while True:
        input_login = input('Enter your login: ')
        input_password = getpass(prompt='Enter your password: ')
        if input_login and input_password:
            break
    users_dict[input_login] = input_password
    write_dict_to_file(users_dict)


def read_dict_from_file(file_name):
    """
    Convert string from a file to a dictionary
    :param: file_name: looks like 'pass.txt'
    :return: decrypted dictionary
    """
    users_str = read_from_file(file_name)
    dictionary = json.loads(users_str)
    for key, value in dictionary.items():
        dictionary[key] = encrypt_string(value, get_key(2, encryption_key))
    return dictionary


def write_dict_to_file(dictionary):
    """
    Convert a dictionary to the string and encrypt it then write to the file
    :param dictionary: dictionary which need to move to the file
    """
    for key, value in dictionary.items():
        dictionary[key] = encrypt_string(value, get_key(1, encryption_key))
    write_to_file('pass.txt', json.dumps(dictionary))


def access_check(user_login, user_password):
    """
    Here we can check if user has the right to login
    :param user_login: Login which was entered by user
    :param user_password: Password which was entered by user
    """
    global users_dict
    if user_login == '':
        raise RuntimeError('Username is empty!')
    if user_login not in users_dict:
        print('You are not registered!!')
        if input('Do you want to register? Type "Yes"\n') == 'yes' or 'y' or '+':
            create_new_user()
            users_dict = read_dict_from_file('pass.txt')
            user_login, user_password = ask_credentials()
        else:
            exit()
    if user_login in users_dict and users_dict[user_login] == user_password:
        print('Access granted')
        new_pass = user_password
        while not new_pass.isalnum():
            print('You have wrong password. Change it again')
            new_pass = getpass(prompt='New password: ')
            users_dict[user_login] = new_pass
            write_dict_to_file(users_dict)
    else:
        print('Access Denied')


try:
    encryption_key = int(read_from_file('key.txt'))
    users_dict = read_dict_from_file('pass.txt')
    login, password = ask_credentials()
    access_check(login, password)
except KeyError:
    print('Access Denied')
except NameError:
    print('Variable users is not defined')
except FileNotFoundError:
    print('There is no file "pass.txt"')
except TypeError:
    print('Missing 2 required positional arguments: "user_login" and "user_password"')
