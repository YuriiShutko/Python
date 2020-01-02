from getpass import getpass
from Encrypt_String import read_from_file, write_to_file, encrypt_string, get_key
import json

admins = ['yura', 'admin', 'administrator']


def is_admin(user_login):
    return True if user_login in admins else False


def is_in_dict(user_login):
    return True if user_login in users_dict else print(f'There is no such user like {user_login}')


def select_action():
    print('"1" - Delete user \n"2" - Create new user\n"3" - Make admin\n"4" - Change password')
    action = input('Choose what to do: ')
    if action == '1':
        delete_user(input('Enter the name who must to be deleted: '))
    if action == '2':
        create_new_user()
    if action == '3':
        make_admin(input('Input user name who will be an admin: '))
    if action == '4':
        change_password(input('Input user name whom need to change password: '))


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
        print('Successfully!!!')
    return username, user_pass


def create_new_user():
    """
    This function creates a new user and add him to the users dictionary
    """
    while True:
        input_login = input('Enter registered login: ')
        input_password = getpass(prompt='Enter registered password: ')
        if input_login and input_password:
            break
    users_dict[input_login] = input_password
    write_dict_to_file(users_dict)
    print(f'New user {input_login} has been created!')


def delete_user(del_user_name):
    if is_admin(login) and access and is_in_dict(del_user_name):
        del users_dict[del_user_name]
        write_dict_to_file(users_dict)
        print(f'The user {del_user_name} has been deleted')


def make_admin(new_admin):
    if is_admin(login) and access and is_in_dict(new_admin):
        admins.append(new_admin)
        print(f'User {new_admin} has been added to admins group')


def change_password(mutable_user_name):
    new_password = ''
    if is_admin(login) and access and is_in_dict(mutable_user_name):
        while new_password == '':
            new_password = getpass(prompt='New password: ')
        users_dict[mutable_user_name] = new_password
        write_dict_to_file(users_dict)
        print(f'Password for {mutable_user_name} has been changed!')


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
    access = access_check(login, password)
    if is_admin(login):
        select_action()
except FileNotFoundError:
    print('There is no file "pass.txt"')
except KeyError:
    print('You are not registered!!')
    if input('Do you want to register? Type "Yes"\n') == 'yes' or 'y' or '+':
        create_new_user()
        users_dict = read_dict_from_file('pass.txt')
        login, password = ask_credentials('You can try to login: ')
        access_check(login, password)
    else:
        exit()

