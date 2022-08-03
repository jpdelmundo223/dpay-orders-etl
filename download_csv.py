from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import configparser
from datetime import timedelta
from datetime import datetime
import time
import shutil
import os
import re
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

options = Options()

# https://stackoverflow.com/questions/45631715/downloading-with-chrome-headless-and-selenium
# chrome_prefs = {"download.default_directory": config.get('shutil', 'source_path')}
# options.add_argument('--headless')
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.experimental_options['prefs'] = chrome_prefs

# https://www.youtube.com/watch?v=Rx66lkB7M74
# This will allow to click the download button/files in headless mode
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

params = {'behavior': 'allow', 'downloadPath': config.get('shutil', 'source_path')}

config = configparser.ConfigParser()
config.read('config.cfg')

dt = datetime.now()

two_days_from_now = dt - timedelta(days=3)
from_date = datetime.strftime(two_days_from_now, "%m/%d/%Y")

to_date = datetime.strftime(dt, "%m/%d/%Y")

def download_csv(url: str, username: str, password: str) -> None:
    driver = webdriver.Chrome(executable_path=r".\chromedriver\chromedriver.exe", options=options)
    # https://www.youtube.com/watch?v=Rx66lkB7M74
    # This will allow to click the download button/files in headless mode
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    
    # Explicitly wait 20 seconds for the element to appear
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_UserId')))
        user_input = driver.find_element(By.ID, 'ContentPlaceHolder1_UserId')
        user_input.send_keys(username)
    except Exception as e:
        print(e)

    # Explicitly wait 20 seconds for the element to appear
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_UserPass')))
        password_input = driver.find_element(By.ID, 'ContentPlaceHolder1_UserPass')
        password_input.send_keys(password)
    except Exception as e:
        print(e)
    finally:
        login = driver.find_element(By.ID, 'ContentPlaceHolder1_Button1')
        # Simulate a click
        login.send_keys(Keys.ENTER)

    try:
        wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_FromDateTextBox')))
        from_date_elem = driver.find_element(By.ID, 'ContentPlaceHolder1_FromDateTextBox')
        from_date_elem.clear()
        from_date_elem.send_keys(from_date)
    except Exception as e:
        print(e)

    try:
        wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_ToDateTextBox')))
        to_date_elem = driver.find_element(By.ID, 'ContentPlaceHolder1_ToDateTextBox')
        to_date_elem.clear()
        to_date_elem.send_keys(to_date)
    except Exception as e:
        print(e)    

    try: 
        wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_TimeFromTextBox')))
        time_from_elem = driver.find_element(By.ID, 'ContentPlaceHolder1_TimeFromTextBox')
        time_from_elem.clear()
        time_from_elem.send_keys(str(timedelta(hours=0, minutes=0, seconds=0)))
    except Exception as e:
        print(e)

    try: 
        wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_TimeToTextBox')))
        time_to_elem = driver.find_element(By.ID, 'ContentPlaceHolder1_TimeToTextBox')
        time_to_elem.clear()
        time_to_elem.send_keys(str(timedelta(hours=23, minutes=59, seconds=59)))
    except Exception as e:
        print(e) 

    status_select = Select(driver.find_element(By.ID, 'ContentPlaceHolder1_StatusList'))
    status_select.select_by_value("S")

    time.sleep(2)

    get_reg_trans = driver.find_element(By.ID, 'ContentPlaceHolder1_GetTxnBtn')
    # Simulate a click
    get_reg_trans.send_keys(Keys.ENTER)

    time.sleep(2)

    export_to_csv = driver.find_element(By.ID, 'ContentPlaceHolder1_ExportButton')
    # Simulate a click
    export_to_csv.send_keys(Keys.ENTER)

    time.sleep(2)

    driver.close()
