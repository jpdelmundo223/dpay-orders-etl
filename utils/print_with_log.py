import os
import configparser

config = configparser.ConfigParser()

config.read('config.cfg')


def log(path: str, text: str) -> str:
    try:
        with open(os.path.join(path, 'logs.txt'), 'a') as t:
            t.write(f"{text}\n")
    except Exception as e:
        print(e)
    return text

def print_with_log(text: str) -> str:
    log_path = config.get('logging', 'log_path')
    print(log(path=log_path, text=text))