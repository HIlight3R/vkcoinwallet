import json
import os

DEFAULT_CONFIG = {'key': '', 'uid': 0, 'token': ''}


def prompt() -> dict:
    print('You need to login to use this program.')

    key = input('Enter your merchant key: ')
    uid = int(input('Enter your VK ID: '))
    token = input('Enter your token here: ')

    cfg = DEFAULT_CONFIG
    cfg['key'] = key
    cfg['uid'] = uid
    cfg['token'] = token

    return cfg


def get_path():
    if os.name == 'nt':
        filepath = f'C:\\Users\\{os.environ.get("USERNAME")}\\.vkcw.json'
    elif os.name == 'posix':
        filepath = f'/home/{os.environ.get("USER")}/.vkcw.json'
    else:
        filepath = None
    return filepath


def login() -> dict:
    filepath = get_path()

    if filepath:
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                config = json.load(file)
        else:
            with open(filepath, 'w') as file:
                config = prompt()
                json.dump(config, file)
    else:
        config = prompt()

    return config
