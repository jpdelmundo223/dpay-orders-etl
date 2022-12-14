from download_csv import download_csv
from utils.delete_old_files import delete_old_files
from utils.move_files import copy_files, move_files
from etl import load_to_mssql, load_to_mysql
import configparser
import time
import os

# Read from config file
config = configparser.ConfigParser()
config.read('config.cfg')

# 
url = config.get('dragonpay', 'dpay_admin_url')
user = config.get('dragonpay', 'dpay_admin_user', fallback='CNEBOOKSHOP')
password = config.get('dragonpay', 'dpay_admin_password', fallback='h6LR5tFc8xeP5aM')
source_path = config.get('shutil', 'source_path')
destination_path = config.get('shutil', 'destination_path')
csv_path = config.get('csv', 'csv_path')


if __name__ == "__main__":
    # Create csv folder if not exists
    if not os.path.exists(os.path.basename(csv_path)):
        os.mkdir(os.path.join(os.path.dirname(__file__), os.path.basename(csv_path)))

    download_csv(url=url, username=user, password=password)
    time.sleep(2)
    copy_files(src=source_path, dst=destination_path)
    delete_old_files(src=source_path, pattern='txnlist', days=1)
    load_to_mssql()
    load_to_mysql()
    delete_old_files(src=csv_path, pattern='txnlist', days=1)