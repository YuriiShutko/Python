from getpass import getpass
from Encrypt_String import read_from_file, write_to_file, encrypt_string, get_key
import json

admins = ['yura', 'admin', 'administrator']


def is_admin(user_login):
    return True if user_login in admins else False


def ask_credentials(message):
    """
    This function ask user to enter his credentials
    :return: Returns a tuple with the following (username, user_pass)
    """
    print(message)
    username = user_pass = ''
    while not username or not user_pass:
        username = input('Login: ')
        user_pass = getpass(prompt='Password: ')
    else:
        print('Credentials were entered')
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


def delete_user(user_login, del_user_name, signed_in):
    if is_admin(user_login) and signed_in:
        del users_dict[del_user_name]
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
    print(dictionary)
    return dictionary


def write_dict_to_file(dictionary):
    """
    Convert a dictionary to the string and encrypt it then write to the file
    :param dictionary: dictionary which need to move to the file
    """
    for key, value in dictionary.items():
        dictionary[key] = encrypt_string(value, get_key(1, encryption_key))
    write_to_file('pass.txt', json.dumps(dictionary))


def check_password_policy(user_login, user_password):
    """
    Checking password's policy
    :param user_login: Login which was entered by user
    :param user_password: Password which was entered by user
    """
    new_pass = user_password
    while not new_pass.isalnum():
        print('You have wrong password. Change it again')
        new_pass = getpass(prompt='New password: ')
        users_dict[user_login] = new_pass
    if user_password != new_pass:
        write_dict_to_file(users_dict)


def access_check(user_login, user_password):
    if user_login in users_dict and users_dict[user_login] == user_password:
        print('Access granted')
        check_password_policy(user_login, user_password)
        return True
    elif user_login not in users_dict:
        raise KeyError
    else:
        print('Access Denied')
        return False


try:
    encryption_key = int(read_from_file('key.txt'))
    users_dict = read_dict_from_file('pass.txt')
    login, password = ask_credentials('Enter your credentials please: ')
    access_check(login, password)
except KeyError:
    print('You are not registered!!')
    if input('Do you want to register? Type "Yes"\n') == 'yes' or 'y' or '+':
        create_new_user()
        users_dict = read_dict_from_file('pass.txt')
        login, password = ask_credentials('You can try to login: ')
        access_check(login, password)
    else:
        exit()
except NameError:
    print('Variable users is not defined')
except FileNotFoundError:
    print('There is no file "pass.txt"')
except TypeError:
    print('Missing 2 required positional arguments: "user_login" and "user_password"')
