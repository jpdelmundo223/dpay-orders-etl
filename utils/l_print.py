import os
import configparser

# Read from config file
config = configparser.ConfigParser()
config.read('config.cfg')

def log(path: str, text: str) -> str:
    try:
        with open(os.path.join(path, 'logs.log'), 'a') as t:
            t.write(f"{text}\n")
    except Exception as e:
        print(e)
    return text

def l_print(text: str) -> str:
    log_path = config.get('logging', 'log_path')
    print(log(path=log_path, text=text))